import streamlit as st
import sqlite3
import pandas as pd

@st.cache_resource(show_spinner=False)
def get_connection():
    return sqlite3.connect("mydatabase.db", check_same_thread=False)

conn = get_connection()
st.title("Search Tree Inventory")

# Load the full inventory table
inv_df = pd.read_sql_query("SELECT * FROM Nursery_Tree_Inventory", conn)

# 1. Tree Name dropdown (from "tree_common name")
tree_names = inv_df["tree_common name"].dropna().unique().tolist() if not inv_df.empty else []
selected_tree = st.selectbox("Tree Name", [""] + tree_names)

# 2. Minimum Height (m) dropdown (distinct values)
min_heights = sorted(inv_df["Min_height"].dropna().unique().tolist()) if not inv_df.empty else []
selected_min_height = st.selectbox("Minimum Height (m)", [""] + min_heights)

# 3. Maximum Height (m) dropdown (distinct values)
max_heights = sorted(inv_df["Max_height"].dropna().unique().tolist()) if not inv_df.empty else []
selected_max_height = st.selectbox("Maximum Height (m)", [""] + max_heights)

# 4. Packaging Type dropdown
packaging_types = inv_df["Packaging_type"].dropna().unique().tolist() if not inv_df.empty else []
selected_packaging = st.selectbox("Packaging Type", [""] + packaging_types)

query = """
SELECT 
    NTI.Quantity_in_stock,
    T.Scientific_name,
    NTI."tree_common name" AS Tree_Name,
    T.Watering_demand,
    T.Main_Photo_url,
    T.Origin,
    T.Soil_type,
    T.Root_type,
    T.Leafl_Type,
    N.Address,
    NTI.Price,
    T.Growth_rate,
    NTI.Packaging_type,
    NTI.Min_height,
    NTI.Max_height,
    T.shape
FROM Nursery_Tree_Inventory NTI
LEFT JOIN Trees T ON NTI."tree_common name" = T.Common_name
LEFT JOIN Nurseries N ON NTI.nursery_name = N.Nursery_name
WHERE 1=1
"""
params = []
if selected_tree:
    query += ' AND NTI."tree_common name" = ?'
    params.append(selected_tree)
if selected_min_height:
    query += ' AND NTI.Min_height = ?'
    params.append(selected_min_height)
if selected_max_height:
    query += ' AND NTI.Max_height = ?'
    params.append(selected_max_height)
if selected_packaging:
    query += ' AND NTI.Packaging_type = ?'
    params.append(selected_packaging)

result_df = pd.read_sql_query(query, conn, params=params)

st.markdown("#### Search Results")
if result_df.empty:
    st.info("No records found for the selected criteria.")
else:
    display_cols = [
        "Tree_Name", "Quantity_in_stock", "Scientific_name", "shape", "Watering_demand",
        "Main_Photo_url", "Origin", "Soil_type", "Root_type", "Leafl_Type", "Address",
        "Price", "Growth_rate", "Min_height", "Max_height", "Packaging_type"
    ]
    st.dataframe(result_df[display_cols])
