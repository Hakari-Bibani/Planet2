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
    .stSlider > div {
        padding: 10px 0;
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
    
    # Dynamic Height Range Dashboard based on available data for the selected tree
    if selected_tree != "All":
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        height_range = run_query(height_range_query, (selected_tree,))
    else:
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory;"
        height_range = run_query(height_range_query)
        
    if height_range and height_range[0]['min_val'] is not None and height_range[0]['max_val'] is not None:
        slider_min = float(height_range[0]['min_val'])
        slider_max = float(height_range[0]['max_val'])
        selected_height_range = st.slider("Select Height Range (cm)", min_value=slider_min, max_value=slider_max, value=(slider_min, slider_max))
    else:
        selected_height_range = None

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
        if selected_height_range:
            conditions.append("nti.min_height >= %s AND nti.max_height <= %s")
            params.extend([selected_height_range[0], selected_height_range[1]])
        
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
                # Reorder columns to show height data prominently and rename for clarity
                ordered_cols = ['quantity_in_stock', 'price', 'min_height', 'max_height', 'growth_rate', 'scientific_name', 'shape', 'watering_demand', 'main_photo_url', 'origin', 'soil_type', 'root_type', 'leafl_type', 'address']
                df = df[ordered_cols]
                df.rename(columns={'min_height': 'Minimum Height (cm)', 'max_height': 'Maximum Height (cm)'}, inplace=True)
                st.dataframe(df)
            else:
                st.write("No results found.")
        else:
            st.write("Please select at least one filter.")
