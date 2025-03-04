import streamlit as st
from handle import run_query, fetch_dataframe

def add_inventory(data):
    query = """
    INSERT INTO "Nursery_Tree_Inventory" 
    ("nursery_name", "tree_common_name", "Quantity_in_stock", "Min_height", "Max_height", "Packaging_type", "Price", "Date")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data.get("nursery_name"), data.get("tree_common_name"), data.get("Quantity_in_stock"),
        data.get("Min_height"), data.get("Max_height"), data.get("Packaging_type"),
        data.get("Price"), data.get("Date")
    )
    run_query(query, params)

def get_all_inventory():
    query = 'SELECT * FROM "Nursery_Tree_Inventory"'
    return fetch_dataframe(query)

def inventory_data_entry():
    st.subheader("Nursery Tree Inventory Entry (Single)")
    with st.form("inventory_entry_form"):
        # Dropdown for nursery_name from Nurseries table:
        from Nurseries import get_all_nurseries
        df_nurseries = get_all_nurseries()
        nursery_names = df_nurseries["Nursery_name"].dropna().unique().tolist() if not df_nurseries.empty else []
        nursery_name = st.selectbox("Nursery Name", options=nursery_names)
        
        # Dropdown for tree_common_name from Trees table:
        from trees import get_all_trees
        df_trees = get_all_trees()
        tree_common_names = df_trees["Common_name"].dropna().unique().tolist() if not df_trees.empty else []
        tree_common_name = st.selectbox("Tree Common Name", options=tree_common_names)
        
        quantity_in_stock = st.number_input("Quantity in Stock", min_value=0)
        min_height = st.number_input("Minimum Height (m)", min_value=0.0, format="%.2f")
        max_height = st.number_input("Maximum Height (m)", min_value=0.0, format="%.2f")
        
        # Packaging_type dropdown: show existing values from inventory
        df_inventory = get_all_inventory()
        packaging_types = df_inventory["Packaging_type"].dropna().unique().tolist() if not df_inventory.empty else []
        packaging_choice = st.selectbox("Select Existing Packaging Type", options=[""] + packaging_types)
        packaging_type = packaging_choice if packaging_choice != "" else st.text_input("Enter Packaging Type")
        
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        date = st.date_input("Date")
        
        submitted = st.form_submit_button("Add Inventory")
        if submitted:
            data = {
                "nursery_name": nursery_name,
                "tree_common_name": tree_common_name,
                "Quantity_in_stock": quantity_in_stock,
                "Min_height": min_height,
                "Max_height": max_height,
                "Packaging_type": packaging_type,
                "Price": price,
                "Date": date,
            }
            add_inventory(data)
            st.success("Inventory added successfully!")
