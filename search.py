import streamlit as st
import pandas as pd
from handle import run_query

def search_page():
    """
    Professional search page for inventory with advanced styling and user experience.
    """
    # Custom CSS for enhanced professional design
    st.markdown("""
    <style>
    /* Page Title Styling */
    .page-title {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 2px solid #007bff;
        margin-bottom: 20px;
    }

    /* Selectbox and Slider Styling */
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {
        background-color: #f8f9fa;
        border: 1.5px solid #ced4da;
        border-radius: 6px;
        padding: 10px;
        color: #495057;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div > div:hover,
    .stSlider > div > div > div:hover {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25);
    }

    /* Search Button Styling */
    .stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 6px;
        font-weight: 600;
        text-transform: uppercase;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #0056b3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Results Table Styling */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background-color: white;
    }

    .dataframe th {
        background-color: #f8f9fa;
        color: #2c3e50;
        font-weight: 600;
        border: 1px solid #dee2e6;
        padding: 12px;
        text-align: left;
    }

    .dataframe td {
        border: 1px solid #dee2e6;
        padding: 10px;
        color: #495057;
    }

    /* Height Range Card Styling */
    .height-range-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .height-range-title {
        color: #2c3e50;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Professional title with custom styling
    st.markdown('<h1 class="page-title">Search Inventory</h1>', unsafe_allow_html=True)
    
    # Dropdown for Tree Name from Nursery_Tree_Inventory
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    
    # Dropdown for Packaging Type from Nursery_Tree_Inventory
    query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
    packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
    
    # Create two columns for dropdown selectors
    col1, col2 = st.columns(2)
    
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)

    # Height Range Selector
    if selected_tree != "All":
        # Get height range for selected tree
        height_query = """
        SELECT 
            MIN(t.height) as min_height,
            MAX(t.height) as max_height
        FROM Nursery_Tree_Inventory nti
        JOIN Trees t ON nti.tree_common_name = t.common_name
        WHERE nti.tree_common_name = %s;
        """
        height_data = run_query(height_query, (selected_tree,))
        
        if height_data and height_data[0]['min_height'] is not None:
            min_height = float(height_data[0]['min_height'])
            max_height = float(height_data[0]['max_height'])
            
            st.markdown('<div class="height-range-card">', unsafe_allow_html=True)
            st.markdown('<div class="height-range-title">Height Range (meters)</div>', unsafe_allow_html=True)
            
            height_range = st.slider(
                "Select Height Range",
                min_value=min_height,
                max_value=max_height,
                value=(min_height, max_height),
                step=0.1,
                key="height_range"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Search Button with Full Width
    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
            if 'height_range' in st.session_state:
                conditions.append("t.height BETWEEN %s AND %s")
                params.extend(st.session_state.height_range)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        
        if conditions:
            where_clause = " AND ".join(conditions)
            query = f"""
            SELECT 
                nti.tree_common_name as "Tree Name",
                t.height as "Height (m)",
                nti.quantity_in_stock as "Stock",
                nti.price as "Price",
                t.growth_rate as "Growth Rate",
                t.scientific_name as "Scientific Name",
                t.shape as "Shape",
                t.watering_demand as "Water Demand",
                t.origin as "Origin",
                t.soil_type as "Soil Type",
                t.root_type as "Root Type",
                t.leafl_type as "Leaf Type",
                n.address as "Nursery Address"
            FROM Nursery_Tree_Inventory nti
            JOIN Trees t ON nti.tree_common_name = t.common_name
            JOIN Nurseries n ON nti.nursery_name = n.nursery_name
            WHERE {where_clause}
            ORDER BY t.height;
            """
            results = run_query(query, tuple(params))
            if results:
                df = pd.DataFrame(results)
                
                # Format height values
                if 'Height (m)' in df.columns:
                    df['Height (m)'] = df['Height (m)'].apply(lambda x: f"{float(x):.1f}")
                
                # Display results in a clean table format
                st.markdown("### Search Results")
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Display height statistics
                if 'Height (m)' in df.columns:
                    stats_col1, stats_col2 = st.columns(2)
                    with stats_col1:
                        st.info(f"Minimum Height: {df['Height (m)'].min()} m")
                    with stats_col2:
                        st.info(f"Maximum Height: {df['Height (m)'].max()} m")
            else:
                st.warning("No results found.")
        else:
            st.info("Please select at least one filter.")
