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

    .stSelectbox > div > div > div:hover {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25);
    }

    /* Slider Styling */
    div[data-baseweb="slider"] {
        margin: 20px 0;
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

    /* Dataframe Styling */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
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
    
    # Retrieve height bounds based on selected tree (or overall if "All")
    if selected_tree != "All":
        query_bounds = "SELECT MIN(min_height) AS min_val, MAX(max_height) AS max_val FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        bounds = run_query(query_bounds, (selected_tree,))
    else:
        query_bounds = "SELECT MIN(min_height) AS min_val, MAX(max_height) AS max_val FROM Nursery_Tree_Inventory;"
        bounds = run_query(query_bounds)
    
    if bounds and bounds[0]['min_val'] is not None and bounds[0]['max_val'] is not None:
        min_bound = float(bounds[0]['min_val'])
        max_bound = float(bounds[0]['max_val'])
        col3, col4 = st.columns(2)
        with col3:
            selected_min_height = st.slider("Minimum Height", min_value=min_bound, max_value=max_bound, value=min_bound, step=0.1)
        with col4:
            selected_max_height = st.slider("Maximum Height", min_value=min_bound, max_value=max_bound, value=max_bound, step=0.1)
    else:
        selected_min_height = None
        selected_max_height = None
    
    # Search Button with Full Width
    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        if selected_min_height is not None and selected_max_height is not None:
            conditions.append("nti.min_height >= %s")
            params.append(selected_min_height)
            conditions.append("nti.max_height <= %s")
            params.append(selected_max_height)
        
        if conditions:
            where_clause = " AND ".join(conditions)
            query = f"""
            SELECT nti.quantity_in_stock, nti.price, nti.min_height, nti.max_height,
                   t.growth_rate, t.scientific_name, t.shape, t.watering_demand, 
                   t.main_photo_url, t.origin, t.soil_type, t.root_type, t.leafl_type, 
                   n.address
            FROM Nursery_Tree_Inventory nti
            JOIN Trees t ON nti.tree_common_name = t.common_name
            JOIN Nurseries n ON nti.nursery_name = n.nursery_name
            WHERE {where_clause};
            """
            results = run_query(query, tuple(params))
            if results:
                df = pd.DataFrame(results)
                st.markdown('<h2 style="text-align: center; color: #2c3e50;">Inventory Results</h2>', unsafe_allow_html=True)
                st.dataframe(df)
            else:
                st.write("No results found.")
        else:
            st.write("Please select at least one filter.")
