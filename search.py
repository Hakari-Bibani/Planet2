import streamlit as st
import pandas as pd
from handle import run_query

def search_page():
    """
    Professional search page for inventory with advanced styling and user experience.
    """
    # Custom CSS for professional design
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

    /* Card Container */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Selectbox and Slider Styling */
    .stSelectbox > div > div > div {
        background-color: #f8f9fa;
        border: 1.5px solid #ced4da;
        border-radius: 6px;
        padding: 10px;
        color: #495057;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div > div:hover {
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
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #0056b3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Enhanced Table Styling */
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        width: 100%;
    }

    .styled-table thead tr {
        background-color: #007bff;
        color: white;
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

    /* Dashboard Card */
    .dashboard-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }

    /* Section Headers */
    .section-header {
        color: #2c3e50;
        font-size: 1.2em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Professional title with custom styling
    st.markdown('<h1 class="page-title">Search Inventory</h1>', unsafe_allow_html=True)
    
    # Get height range from database
    height_query = """
    SELECT 
        MIN(t.height) as min_height,
        MAX(t.height) as max_height
    FROM Trees t
    JOIN Nursery_Tree_Inventory nti ON t.common_name = nti.tree_common_name;
    """
    
    try:
        height_results = run_query(height_query)
        min_height = float(height_results[0]['min_height']) if height_results and height_results[0]['min_height'] else 0
        max_height = float(height_results[0]['max_height']) if height_results and height_results[0]['max_height'] else 100
    except Exception:
        # Fallback values if query fails
        min_height = 0
        max_height = 100
    
    # Dropdown for Tree Name from Nursery_Tree_Inventory
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    
    # Dropdown for Packaging Type from Nursery_Tree_Inventory
    query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
    packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
    
    # Dashboard Layout
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    
    # Create columns for filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">Tree Selection</p>', unsafe_allow_html=True)
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    
    with col2:
        st.markdown('<p class="section-header">Packaging</p>', unsafe_allow_html=True)
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)
    
    # Height Range Slider
    st.markdown('<p class="section-header">Height Range (feet)</p>', unsafe_allow_html=True)
    height_range = st.slider(
        "Select Height Range",
        min_value=float(min_height),
        max_value=float(max_height),
        value=(float(min_height), float(max_height)),
        step=0.5
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search Button
    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
            
        # Add height range condition
        conditions.append("t.height BETWEEN %s AND %s")
        params.extend([height_range[0], height_range[1]])
        
        where_clause = " AND ".join(conditions)
        query = f"""
        SELECT 
            nti.tree_common_name as "Tree Name",
            nti.quantity_in_stock as "Stock",
            nti.price as "Price",
            t.height as "Height",
            t.growth_rate as "Growth Rate",
            t.scientific_name as "Scientific Name",
            t.shape as "Shape",
            t.watering_demand as "Watering",
            n.address as "Nursery Location"
        FROM Nursery_Tree_Inventory nti
        JOIN Trees t ON nti.tree_common_name = t.common_name
        JOIN Nurseries n ON nti.nursery_name = n.nursery_name
        WHERE {where_clause}
        ORDER BY nti.tree_common_name;
        """
        
        results = run_query(query, tuple(params))
        if results:
            df = pd.DataFrame(results)
            
            # Custom table styling
            st.markdown('<div style="overflow-x: auto;">', unsafe_allow_html=True)
            st.markdown(
                df.style
                .set_properties(**{
                    'background-color': '#f8f9fa',
                    'color': '#2c3e50',
                    'border': '1px solid #dee2e6',
                    'text-align': 'left',
                    'padding': '12px 15px'
                })
                .set_table_styles([
                    {'selector': 'thead th',
                     'props': [('background-color', '#007bff'),
                              ('color', 'white'),
                              ('font-weight', 'bold')]},
                    {'selector': 'tbody tr:nth-of-type(even)',
                     'props': [('background-color', '#ffffff')]},
                ])
                .to_html(), unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No results found matching your criteria.")
