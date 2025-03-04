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

    /* Selectbox Styling */
    .stSelectbox > div > div > div {
        background-color: #f8f9fa;
        border: 1.5px solid #ced4da;
        border-radius: 6px;
        padding: 10px;
        color: #495057;
        transition: all 0.3s ease;
    }

    /* Slider Styling */
    .stSlider .thumb {
        background-color: #007bff !important;
    }
    .stSlider .track {
        background-color: #007bff33 !important;
    }

    /* Data Table Styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.95em;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    .styled-table thead tr {
        background-color: #007bff;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, 
    .styled-table td {
        padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f8f9fa;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #007bff;
    }
    .height-badge {
        background-color: #007bff;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">🌳 Advanced Tree Inventory Search</h1>', unsafe_allow_html=True)
    
    # Get tree names and packaging types
    tree_names = [row["tree_common_name"] for row in run_query("SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;") or []]
    packaging_types = [row["packaging_type"] for row in run_query("SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;") or []]

    # Layout columns
    col1, col2 = st.columns(2)
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)

    # Get height range based on selection
    if selected_tree != "All":
        height_query = f"""
        SELECT MIN(t.min_height) as min_h, MAX(t.max_height) as max_h 
        FROM Trees t
        WHERE t.common_name = '{selected_tree}'
        """
    else:
        height_query = "SELECT MIN(min_height) as min_h, MAX(max_height) as max_h FROM Trees"
    
    height_data = run_query(height_query)[0]
    min_h, max_h = height_data['min_h'] or 0, height_data['max_h'] or 100

    # Height range slider
    st.markdown("### 🌱 Height Range Filter")
    height_range = st.slider(
        "Select height range (meters)", 
        min_value=float(min_h), 
        max_value=float(max_h),
        value=(float(min_h), float(max_h)),
        help="Adjust to filter by tree height range"
    )

    # Search functionality
    if st.button("🔍 Search Inventory", use_container_width=True):
        conditions = []
        params = []
        
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        
        # Add height conditions
        conditions.append("t.min_height >= %s AND t.max_height <= %s")
        params.extend([height_range[0], height_range[1]])

        query = f"""
        SELECT nti.quantity_in_stock, nti.price, 
               t.growth_rate, t.scientific_name, t.shape, t.watering_demand,
               t.main_photo_url, t.origin, t.soil_type, t.root_type, t.leafl_type,
               n.address, t.min_height, t.max_height
        FROM Nursery_Tree_Inventory nti
        JOIN Trees t ON nti.tree_common_name = t.common_name
        JOIN Nurseries n ON nti.nursery_name = n.nursery_name
        WHERE {' AND '.join(conditions)}
        """
        
        results = run_query(query, tuple(params))
        if results:
            df = pd.DataFrame(results)
            # Format height columns
            df['Minimum Height'] = df['min_height'].apply(lambda x: f'<span class="height-badge">{x}m</span>')
            df['Maximum Height'] = df['max_height'].apply(lambda x: f'<span class="height-badge">{x}m</span>')
            df.drop(['min_height', 'max_height'], axis=1, inplace=True)
            
            # Display styled table
            st.markdown(df.to_html(escape=False, classes='styled-table', index=False), unsafe_allow_html=True)
        else:
            st.warning("No matching results found. Showing all available entries:")
            fallback_query = "SELECT * FROM Nursery_Tree_Inventory LIMIT 10"
            fallback_results = run_query(fallback_query)
            if fallback_results:
                st.dataframe(pd.DataFrame(fallback_results))

# Note: Ensure your database schema includes min_height and max_height columns in the Trees table
