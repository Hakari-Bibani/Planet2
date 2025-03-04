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
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
    }

    .dataframe th {
        background-color: #007bff;
        color: white;
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
    
    # Query to get global minimum and maximum height boundaries
    query_height = "SELECT MIN(min_height) AS global_min, MAX(max_height) AS global_max FROM Nursery_Tree_Inventory;"
    height_data = run_query(query_height)
    if height_data:
        global_min = height_data[0]["global_min"]
        global_max = height_data[0]["global_max"]
    else:
        global_min, global_max = 0, 0
    
    # Height range slider dashboard
    selected_height = st.slider("Select Height Range (Min - Max)", 
                                min_value=float(global_min), 
                                max_value=float(global_max), 
                                value=(float(global_min), float(global_max)))
    
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
        
        # Add height range conditions
        conditions.append("nti.min_height >= %s")
        params.append(selected_height[0])
        conditions.append("nti.max_height <= %s")
        params.append(selected_height[1])
        
        where_clause = " AND ".join(conditions)
        query = f"""
            SELECT nti.quantity_in_stock, nti.price, 
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
            st.markdown('<h2 style="color:#2c3e50; text-align:center; margin-top:20px;">Search Results</h2>', unsafe_allow_html=True)
            # Display the table with professional styling using pandas styling
            styled_df = df.style.set_table_styles([
                {"selector": "thead", "props": [("background-color", "#007bff"), ("color", "white"), ("text-align", "center")]},
                {"selector": "tbody tr", "props": [("background-color", "#f8f9fa"), ("color", "#495057")]}
            ])
            st.write(styled_df)
        else:
            st.write("No results found.")
