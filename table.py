import streamlit as st
import nurseries
import trees
import inventory

def data_entry_page():
    st.title("Data Entry")
    table_option = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory"])
    entry_type = st.radio("Select Entry Type", ["Single Entry", "Bulk Entry", "Modify/Delete"])
    if table_option == "Nurseries":
        nurseries.handle_nurseries(entry_type)
    elif table_option == "Trees":
        trees.handle_trees(entry_type)
    elif table_option == "Nursery_Tree_Inventory":
        inventory.handle_inventory(entry_type)
