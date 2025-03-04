import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

def handle_inventory(entry_type):
    if entry_type == "Single Entry":
        st.subheader("Add Single Nursery Tree Inventory")
        nursery_query = "SELECT nursery_name FROM Nurseries;"
        nurseries = [row["nursery_name"] for row in run_query(nursery_query) or []]
        nursery_name = st.selectbox("Nursery Name", nurseries)
        tree_query = "SELECT common_name FROM Trees;"
        tree_names = [row["common_name"] for row in run_query(tree_query) or []]
        tree_common_name = st.selectbox("Tree Common Name", tree_names)
        quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1)
        min_height = st.number_input("Minimum Height", value=0.0)
        max_height = st.number_input("Maximum Height", value=0.0)
        packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
        packaging_choice = st.selectbox("Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"])
        packaging_type = st.text_input("Enter Packaging Type") if packaging_choice == "Add New" else packaging_choice
        price = st.number_input("Price (IQD)", value=0.0)
        date = st.date_input("Date")
        if st.button("Add Inventory Record"):
            query = """
            INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date))
            st.success("Inventory record added!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Nursery Tree Inventory")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()  # ensure headers are lower-case
            for index, row in df.iterrows():
                query = """
                INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (
                    row["nursery_name"],
                    row["tree_common_name"],
                    row["quantity_in_stock"],
                    row["min_height"],
                    row["max_height"],
                    row["packaging_type"],
                    row["price"],
                    row["date"]
                ))
            st.success("Bulk inventory records added!")
    elif entry_type == "Modify/Delete":
        st.subheader("Modify/Delete Nursery Tree Inventory")
        query = "SELECT * FROM Nursery_Tree_Inventory;"
        data = run_query(query)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            selected_id = st.selectbox("Select Inventory ID to Modify/Delete", df["tree_inventory_id"])
            action = st.radio("Action", ["Modify", "Delete"])
            if action == "Delete":
                if st.button("Delete Inventory Record"):
                    delete_query = "DELETE FROM Nursery_Tree_Inventory WHERE tree_inventory_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("Inventory record deleted!")
            else:
                row = df[df["tree_inventory_id"] == selected_id].iloc[0]
                nursery_query = "SELECT nursery_name FROM Nurseries;"
                nurseries = [r["nursery_name"] for r in run_query(nursery_query) or []]
                nursery_name = st.selectbox("Nursery Name", nurseries, index=nurseries.index(row["nursery_name"]) if row["nursery_name"] in nurseries else 0)
                tree_query = "SELECT common_name FROM Trees;"
                tree_names = [r["common_name"] for r in run_query(tree_query) or []]
                tree_common_name = st.selectbox("Tree Common Name", tree_names, index=tree_names.index(row["tree_common_name"]) if row["tree_common_name"] in tree_names else 0)
                quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1, value=row["quantity_in_stock"])
                min_height = st.number_input("Minimum Height", value=float(row["min_height"]))
                max_height = st.number_input("Maximum Height", value=float(row["max_height"]))
                packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
                packaging_choice = st.selectbox("Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"], index=0)
                packaging_type = st.text_input("Enter Packaging Type", value=row["packaging_type"]) if packaging_choice == "Add New" else packaging_choice
                price = st.number_input("Price (IQD)", value=float(row["price"]))
                date = st.date_input("Date", value=pd.to_datetime(row["date"]))
                if st.button("Update Inventory Record"):
                    update_query = """
                    UPDATE Nursery_Tree_Inventory SET nursery_name=%s, tree_common_name=%s, quantity_in_stock=%s, 
                    min_height=%s, max_height=%s, packaging_type=%s, price=%s, date=%s
                    WHERE tree_inventory_id=%s;
                    """
                    execute_query(update_query, (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date, selected_id))
                    st.success("Inventory record updated!")
