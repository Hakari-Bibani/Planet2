import streamlit as st
import nurseries
import trees
import inventory

def data_entry_page():
    st.title("Data Entry")
    table_option = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory", "Payments"])
    if table_option == "Payments":
    import payment
    payment.handle_payments("Modify/Delete")

    tab1, tab2, tab3 = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])

    if table_option == "Nurseries":
        with tab1:
            nurseries.handle_nurseries("Single Entry")
        with tab2:
            nurseries.handle_nurseries("Bulk Entry")
        with tab3:
            nurseries.handle_nurseries("Modify/Delete")
    elif table_option == "Trees":
        with tab1:
            trees.handle_trees("Single Entry")
        with tab2:
            trees.handle_trees("Bulk Entry")
        with tab3:
            trees.handle_trees("Modify/Delete")
    elif table_option == "Nursery_Tree_Inventory":
        with tab1:
            inventory.handle_inventory("Single Entry")
        with tab2:
            inventory.handle_inventory("Bulk Entry")
        with tab3:
            inventory.handle_inventory("Modify/Delete")
