import streamlit as st
import sqlite3
import pandas as pd

# Function to get database connection
def get_connection():
    return sqlite3.connect("mydatabase.db", check_same_thread=False)

conn = get_connection()
st.title("Research Page - Inventory Search")

st.header("Search Tree Inventory")

# Load the full inventory table
inventory_df = pd.read_sql_query("SELECT * FROM Nursery_Tree_Inventory", conn)

# 1. Tree Name dropdown (from "tree_common name")
tree_names = inventory_df["tree_common name"].dropna().unique().tolist() if not inventory_df.empty else []
selected_tree = st.selectbox("Tree Name", options=[""] + tree_names)

# 2. Minimum Height (m) dropdown (using distinct values from Min_height)
min_heights = sorted(inventory_df["Min_height"].dropna().unique().tolist()) if not inventory_df.empty else []
selected_min_height = st.selectbox("Minimum Height (m)", options=[""] + min_heights)

# 3. Maximum Height (m) dropdown (using distinct values from Max_height)
max_heights = sorted(inventory_df["Max_height"].dropna().unique().tolist()) if not inventory_df.empty else []
selected_max_height = st.selectbox("Maximum Height (m)", options=[""] + max_heights)

# 4. Packaging Type dropdown
packaging_types = inventory_df["Packaging_type"].dropna().unique().tolist() if not inventory_df.empty else []
selected_packaging = st.selectbox("Packaging Type", options=[""] + packaging_types)

# Note: Fields Price, Growth_rate, and Shape are displayed in the results.
# We now construct a query joining the Nursery_Tree_Inventory table with Trees and Nurseries to retrieve additional details.
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

st.subheader("Search Results")
if result_df.empty:
    st.info("No records found for the selected criteria.")
else:
    # Display the requested columns:
    # Quantity_in_stock, Scientific_name, shape, Watering_demand, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type, Address
    display_cols = [
        "Tree_Name", "Quantity_in_stock", "Scientific_name", "shape", "Watering_demand",
        "Main_Photo_url", "Origin", "Soil_type", "Root_type", "Leafl_Type", "Address",
        "Price", "Growth_rate", "Min_height", "Max_height", "Packaging_type"
    ]
    st.dataframe(result_df[display_cols])
