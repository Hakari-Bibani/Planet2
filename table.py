import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

def data_entry_page():
    st.title("Data Entry")
    table_option = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory"])
    entry_type = st.radio("Select Entry Type", ["Single Entry", "Bulk Entry", "Modify/Delete"])
    if table_option == "Nurseries":
        handle_nurseries(entry_type)
    elif table_option == "Trees":
        handle_trees(entry_type)
    elif table_option == "Nursery_Tree_Inventory":
        handle_inventory(entry_type)

def handle_nurseries(entry_type):
    if entry_type == "Single Entry":
        st.subheader("Add Single Nursery")
        Registration_code = st.text_input("Registration Code")
        Nursery_name = st.text_input("Nursery Name")
        Address = st.text_input("Address")
        Contact_name = st.text_input("Contact Name")
        Contact_phone = st.text_input("Contact Phone")
        Google_map_link = st.text_input("Google Map Link")
        Additional_notes = st.text_area("Additional Notes")
        if st.button("Add Nursery"):
            query = """
            INSERT INTO Nurseries (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes))
            st.success("Nursery added successfully!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Nurseries")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                query = """
                INSERT INTO Nurseries (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (row["Registration_code"], row["Nursery_name"], row["Address"], row["Contact_name"], row["Contact_phone"], row["Google_map_link"], row.get("Additional_notes", "")))
            st.success("Bulk nurseries added!")
    elif entry_type == "Modify/Delete":
        st.subheader("Modify/Delete Nurseries")
        query = "SELECT * FROM Nurseries;"
        data = run_query(query)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            selected_id = st.selectbox("Select Nursery ID to Modify/Delete", df["nursery_id"])
            action = st.radio("Action", ["Modify", "Delete"])
            if action == "Delete":
                if st.button("Delete Nursery"):
                    delete_query = "DELETE FROM Nurseries WHERE nursery_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("Nursery deleted!")
            else:
                row = df[df["nursery_id"] == selected_id].iloc[0]
                Registration_code = st.text_input("Registration Code", value=row["Registration_code"])
                Nursery_name = st.text_input("Nursery Name", value=row["Nursery_name"])
                Address = st.text_input("Address", value=row["Address"])
                Contact_name = st.text_input("Contact Name", value=row["Contact_name"])
                Contact_phone = st.text_input("Contact Phone", value=row["Contact_phone"])
                Google_map_link = st.text_input("Google Map Link", value=row["Google_map_link"])
                Additional_notes = st.text_area("Additional Notes", value=row["Additional_notes"])
                if st.button("Update Nursery"):
                    update_query = """
                    UPDATE Nurseries SET Registration_code=%s, Nursery_name=%s, Address=%s, Contact_name=%s, Contact_phone=%s, Google_map_link=%s, Additional_notes=%s
                    WHERE nursery_id=%s;
                    """
                    execute_query(update_query, (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes, selected_id))
                    st.success("Nursery updated!")

def handle_trees(entry_type):
    if entry_type == "Single Entry":
        st.subheader("Add Single Tree")
        Common_name = st.text_input("Common Name")
        Scientific_name = st.text_input("Scientific Name")
        Growth_rate = st.number_input("Growth Rate (cm/yr)", value=0.0)
        Watering_demand = st.text_input("Watering Demand")
        existing_shape = fetch_dropdown("Trees", "shape")
        shape_choice = st.selectbox("Shape", (["Add New"] + existing_shape) if existing_shape else ["Add New"])
        shape = st.text_input("Enter Shape") if shape_choice == "Add New" else shape_choice
        existing_origin = fetch_dropdown("Trees", "Origin")
        origin_choice = st.selectbox("Origin", (["Add New"] + existing_origin) if existing_origin else ["Add New"])
        Origin = st.text_input("Enter Origin") if origin_choice == "Add New" else origin_choice
        existing_soil = fetch_dropdown("Trees", "Soil_type")
        soil_choice = st.selectbox("Soil Type", (["Add New"] + existing_soil) if existing_soil else ["Add New"])
        Soil_type = st.text_input("Enter Soil Type") if soil_choice == "Add New" else soil_choice
        existing_root = fetch_dropdown("Trees", "Root_type")
        root_choice = st.selectbox("Root Type", (["Add New"] + existing_root) if existing_root else ["Add New"])
        Root_type = st.text_input("Enter Root Type") if root_choice == "Add New" else root_choice
        existing_leaf = fetch_dropdown("Trees", "Leafl_Type")
        leaf_choice = st.selectbox("Leaf Type", (["Add New"] + existing_leaf) if existing_leaf else ["Add New"])
        Leafl_Type = st.text_input("Enter Leaf Type") if leaf_choice == "Add New" else leaf_choice
        Care_instructions = st.text_area("Care Instructions")
        Main_Photo_url = st.text_input("Main Photo URL")
        if st.button("Add Tree"):
            query = """
            INSERT INTO Trees (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type))
            st.success("Tree added successfully!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Trees")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                query = """
                INSERT INTO Trees (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (row["Common_name"], row["Scientific_name"], row["Growth_rate"], row["Watering_demand"], row["shape"], row["Care_instructions"], row["Main_Photo_url"], row["Origin"], row["Soil_type"], row["Root_type"], row["Leafl_Type"]))
            st.success("Bulk trees added!")
    elif entry_type == "Modify/Delete":
        st.subheader("Modify/Delete Trees")
        query = "SELECT * FROM Trees;"
        data = run_query(query)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            selected_id = st.selectbox("Select Tree ID to Modify/Delete", df["tree_id"])
            action = st.radio("Action", ["Modify", "Delete"])
            if action == "Delete":
                if st.button("Delete Tree"):
                    delete_query = "DELETE FROM Trees WHERE tree_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("Tree deleted!")
            else:
                row = df[df["tree_id"] == selected_id].iloc[0]
                Common_name = st.text_input("Common Name", value=row["Common_name"])
                Scientific_name = st.text_input("Scientific Name", value=row["Scientific_name"])
                Growth_rate = st.number_input("Growth Rate (cm/yr)", value=float(row["Growth_rate"]))
                Watering_demand = st.text_input("Watering Demand", value=row["Watering_demand"])
                shape = st.text_input("Shape", value=row["shape"])
                Care_instructions = st.text_area("Care Instructions", value=row["Care_instructions"])
                Main_Photo_url = st.text_input("Main Photo URL", value=row["Main_Photo_url"])
                Origin = st.text_input("Origin", value=row["Origin"])
                Soil_type = st.text_input("Soil Type", value=row["Soil_type"])
                Root_type = st.text_input("Root Type", value=row["Root_type"])
                Leafl_Type = st.text_input("Leaf Type", value=row["Leafl_Type"])
                if st.button("Update Tree"):
                    update_query = """
                    UPDATE Trees SET Common_name=%s, Scientific_name=%s, Growth_rate=%s, Watering_demand=%s, shape=%s, 
                    Care_instructions=%s, Main_Photo_url=%s, Origin=%s, Soil_type=%s, Root_type=%s, Leafl_Type=%s
                    WHERE tree_id=%s;
                    """
                    execute_query(update_query, (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type, selected_id))
                    st.success("Tree updated!")

def handle_inventory(entry_type):
    if entry_type == "Single Entry":
        st.subheader("Add Single Nursery Tree Inventory")
        nursery_query = "SELECT Nursery_name FROM Nurseries;"
        nurseries = [row["Nursery_name"] for row in run_query(nursery_query) or []]
        nursery_name = st.selectbox("Nursery Name", nurseries)
        tree_query = "SELECT Common_name FROM Trees;"
        tree_names = [row["Common_name"] for row in run_query(tree_query) or []]
        tree_common_name = st.selectbox("Tree Common Name", tree_names)
        Quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1)
        Min_height = st.number_input("Minimum Height", value=0.0)
        Max_height = st.number_input("Maximum Height", value=0.0)
        packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "Packaging_type")
        packaging_choice = st.selectbox("Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"])
        Packaging_type = st.text_input("Enter Packaging Type") if packaging_choice == "Add New" else packaging_choice
        Price = st.number_input("Price (IQD)", value=0.0)
        Date = st.date_input("Date")
        if st.button("Add Inventory Record"):
            query = """
            INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date))
            st.success("Inventory record added!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Nursery Tree Inventory")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                query = """
                INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (row["nursery_name"], row["tree_common_name"], row["Quantity_in_stock"], row["Min_height"], row["Max_height"], row["Packaging_type"], row["Price"], row["Date"]))
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
                nursery_query = "SELECT Nursery_name FROM Nurseries;"
                nurseries = [r["Nursery_name"] for r in run_query(nursery_query) or []]
                nursery_name = st.selectbox("Nursery Name", nurseries, index=nurseries.index(row["nursery_name"]) if row["nursery_name"] in nurseries else 0)
                tree_query = "SELECT Common_name FROM Trees;"
                tree_names = [r["Common_name"] for r in run_query(tree_query) or []]
                tree_common_name = st.selectbox("Tree Common Name", tree_names, index=tree_names.index(row["tree_common_name"]) if row["tree_common_name"] in tree_names else 0)
                Quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1, value=row["Quantity_in_stock"])
                Min_height = st.number_input("Minimum Height", value=float(row["Min_height"]))
                Max_height = st.number_input("Maximum Height", value=float(row["Max_height"]))
                packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "Packaging_type")
                packaging_choice = st.selectbox("Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"], index=0)
                Packaging_type = st.text_input("Enter Packaging Type", value=row["Packaging_type"]) if packaging_choice == "Add New" else packaging_choice
                Price = st.number_input("Price (IQD)", value=float(row["Price"]))
                Date = st.date_input("Date", value=pd.to_datetime(row["Date"]))
                if st.button("Update Inventory Record"):
                    update_query = """
                    UPDATE Nursery_Tree_Inventory SET nursery_name=%s, tree_common_name=%s, Quantity_in_stock=%s, 
                    Min_height=%s, Max_height=%s, Packaging_type=%s, Price=%s, Date=%s
                    WHERE tree_inventory_id=%s;
                    """
                    execute_query(update_query, (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date, selected_id))
                    st.success("Inventory record updated!")
