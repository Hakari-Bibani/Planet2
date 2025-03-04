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
    
    # Dashboard: Add Minimum and Maximum Height slider based on available data.
    if selected_tree != "All":
        query_range = "SELECT MIN(min_height) AS min_range, MAX(max_height) AS max_range FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        range_result = run_query(query_range, (selected_tree,))
    else:
        query_range = "SELECT MIN(min_height) AS min_range, MAX(max_height) AS max_range FROM Nursery_Tree_Inventory;"
        range_result = run_query(query_range)
    
    if range_result and range_result[0]["min_range"] is not None and range_result[0]["max_range"] is not None:
        range_min = range_result[0]["min_range"]
        range_max = range_result[0]["max_range"]
    else:
        range_min, range_max = 0, 0
    
    height_range = st.slider("Select Height Range (cm)", min_value=range_min, max_value=range_max, value=(range_min, range_max))
    
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
        # Add height range condition to support near or exact data match (records overlapping the selected range)
        conditions.append("nti.min_height <= %s")
        params.append(height_range[1])
        conditions.append("nti.max_height >= %s")
        params.append(height_range[0])
        
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
            # Rename columns for a more professional display
            df.rename(columns={
                "quantity_in_stock": "Quantity In Stock",
                "price": "Price (IQD)",
                "min_height": "Minimum Height (cm)",
                "max_height": "Maximum Height (cm)",
                "growth_rate": "Growth Rate (cm/yr)",
                "scientific_name": "Scientific Name",
                "shape": "Shape",
                "watering_demand": "Watering Demand",
                "main_photo_url": "Main Photo URL",
                "origin": "Origin",
                "soil_type": "Soil Type",
                "root_type": "Root Type",
                "leafl_type": "Leaf Type",
                "address": "Nursery Address"
            }, inplace=True)
            st.dataframe(df)
        else:
            st.write("No results found.")
