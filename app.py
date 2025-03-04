import streamlit as st
from sidebar import show_sidebar

def main():
    st.title("Plant Nursery Management App")
    page = show_sidebar()
    
    if page == "Data Entry":
        st.header("Data Entry")
        # Choose the table to work on
        table = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory"])
        if table == "Nurseries":
            from Nurseries import nursery_data_entry
            nursery_data_entry()
        elif table == "Trees":
            from trees import tree_data_entry
            tree_data_entry()
        elif table == "Nursery_Tree_Inventory":
            from Nursery_Tree_Inventory import inventory_data_entry
            inventory_data_entry()
    
    elif page == "Search":
        st.header("Search Inventory")
        from research import search_page
        search_page()

if __name__ == "__main__":
    main()
