import streamlit as st
import pandas as pd
from handle import run_query

def search_page():
    st.title("Search Inventory")
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    query_packaging = "SELECT DISTINCT Packaging_type FROM Nursery_Tree_Inventory;"
    packaging_types = [row["Packaging_type"] for row in run_query(query_packaging) or []]
    query_heights = "SELECT MIN(Min_height) as min_height, MAX(Max_height) as max_height FROM Nursery_Tree_Inventory;"
    height_range = run_query(query_heights)
    if height_range and height_range[0]["min_height"] is not None:
        min_val = float(height_range[0]["min_height"])
        max_val = float(height_range[0]["max_height"])
    else:
        min_val, max_val = 0, 100

    selected_tree = st.selectbox("Tree Name", ["All"] + tree_names)
    selected_min_height = st.slider("Minimum Height (m)", min_val, max_val, min_val)
    selected_max_height = st.slider("Maximum Height (m)", min_val, max_val, max_val)
    selected_packaging = st.selectbox("Packaging Type", ["All"] + packaging_types)

    if st.button("Search"):
        conditions = []
        params = []
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.Packaging_type = %s")
            params.append(selected_packaging)
        conditions.append("nti.Min_height >= %s")
        params.append(selected_min_height)
        conditions.append("nti.Max_height <= %s")
        params.append(selected_max_height)
        where_clause = " AND ".join(conditions)
        query = f"""
        SELECT nti.Quantity_in_stock, nti.Price, t.Growth_rate, t.shape, t.Scientific_name, 
               t.Watering_demand, t.Main_Photo_url, t.Origin, t.Soil_type, t.Root_type, t.Leafl_Type, n.Address
        FROM Nursery_Tree_Inventory nti
        JOIN Trees t ON nti.tree_common_name = t.Common_name
        JOIN Nurseries n ON nti.nursery_name = n.Nursery_name
        WHERE {where_clause};
        """
        results = run_query(query, tuple(params))
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.write("No results found.")
