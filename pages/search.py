import streamlit as st
import pandas as pd
from db import run_query

def app():
    st.title("Search")
    tree_names = [row[0] for row in run_query("SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory", None)]
    selected_tree = st.selectbox("Tree Name", tree_names)
    min_heights = sorted(list(set([row[0] for row in run_query("SELECT DISTINCT Min_height FROM Nursery_Tree_Inventory", None)])))
    max_heights = sorted(list(set([row[0] for row in run_query("SELECT DISTINCT Max_height FROM Nursery_Tree_Inventory", None)])))
    packaging_types = [row[0] for row in run_query("SELECT DISTINCT Packaging_type FROM Nursery_Tree_Inventory", None) if row[0]]
    selected_min_height = st.selectbox("Minimum Height (m)", min_heights)
    selected_max_height = st.selectbox("Maximum Height (m)", max_heights)
    selected_packaging = st.selectbox("Packaging Type", packaging_types)
    if st.button("Search"):
        query = """
        SELECT nti.Quantity_in_stock, nti.Price, t.Growth_rate, t.shape, t.Scientific_name, t.Watering_demand, t.Main_Photo_url, t.Origin, t.Soil_type, t.Root_type, t.Leafl_Type, n.Address
        FROM Nursery_Tree_Inventory nti
        JOIN Trees t ON nti.tree_common_name = t.Common_name
        JOIN Nurseries n ON nti.nursery_name = n.Nursery_name
        WHERE nti.tree_common_name = %s
        AND nti.Min_height = %s
        AND nti.Max_height = %s
        AND nti.Packaging_type = %s
        """
        result = run_query(query, (selected_tree, selected_min_height, selected_max_height, selected_packaging))
        if result:
            df = pd.DataFrame(result, columns=["Quantity_in_stock","Price","Growth_rate","shape","Scientific_name","Watering_demand","Main_Photo_url","Origin","Soil_type","Root_type","Leafl_Type","Address"])
            st.dataframe(df)
        else:
            st.write("No records found")
