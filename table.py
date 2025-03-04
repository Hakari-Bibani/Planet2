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
        registration_code = st.text_input("Registration Code")
        nursery_name = st.text_input("Nursery Name")
        address = st.text_input("Address")
        contact_name = st.text_input("Contact Name")
        contact_phone = st.text_input("Contact Phone")
        google_map_link = st.text_input("Google Map Link")
        additional_notes = st.text_area("Additional Notes")
        if st.button("Add Nursery"):
            query = """
            INSERT INTO Nurseries (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nursery_name) DO UPDATE SET
                registration_code = EXCLUDED.registration_code,
                address = EXCLUDED.address,
                contact_name = EXCLUDED.contact_name,
                contact_phone = EXCLUDED.contact_phone,
                google_map_link = EXCLUDED.google_map_link,
                additional_notes = EXCLUDED.additional_notes;
            """
            execute_query(query, (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes))
            st.success("Nursery added or updated successfully!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Nurseries")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                query = """
                INSERT INTO Nurseries (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nursery_name) DO UPDATE SET
                    registration_code = EXCLUDED.registration_code,
                    address = EXCLUDED.address,
                    contact_name = EXCLUDED.contact_name,
                    contact_phone = EXCLUDED.contact_phone,
                    google_map_link = EXCLUDED.google_map_link,
                    additional_notes = EXCLUDED.additional_notes;
                """
                execute_query(query, (
                    row["registration_code"],
                    row["nursery_name"],
                    row["address"],
                    row["contact_name"],
                    row["contact_phone"],
                    row["google_map_link"],
                    row.get("additional_notes", "")
                ))
            st.success("Bulk nurseries added or updated!")
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
                registration_code = st.text_input("Registration Code", value=row["registration_code"])
                nursery_name = st.text_input("Nursery Name", value=row["nursery_name"])
                address = st.text_input("Address", value=row["address"])
                contact_name = st.text_input("Contact Name", value=row["contact_name"])
                contact_phone = st.text_input("Contact Phone", value=row["contact_phone"])
                google_map_link = st.text_input("Google Map Link", value=row["google_map_link"])
                additional_notes = st.text_area("Additional Notes", value=row["additional_notes"])
                if st.button("Update Nursery"):
                    update_query = """
                    UPDATE Nurseries SET registration_code=%s, nursery_name=%s, address=%s, contact_name=%s, contact_phone=%s, google_map_link=%s, additional_notes=%s
                    WHERE nursery_id=%s;
                    """
                    execute_query(update_query, (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes, selected_id))
                    st.success("Nursery updated!")

def handle_trees(entry_type):
    if entry_type == "Single Entry":
        st.subheader("Add Single Tree")
        common_name = st.text_input("Common Name")
        scientific_name = st.text_input("Scientific Name")
        growth_rate = st.number_input("Growth Rate (cm/yr)", value=0.0)
        watering_demand = st.text_input("Watering Demand")
        existing_shape = fetch_dropdown("Trees", "shape")
        shape_choice = st.selectbox("Shape", (["Add New"] + existing_shape) if existing_shape else ["Add New"])
        shape = st.text_input("Enter Shape") if shape_choice == "Add New" else shape_choice
        existing_origin = fetch_dropdown("Trees", "origin")
        origin_choice = st.selectbox("Origin", (["Add New"] + existing_origin) if existing_origin else ["Add New"])
        origin = st.text_input("Enter Origin") if origin_choice == "Add New" else origin_choice
        existing_soil = fetch_dropdown("Trees", "soil_type")
        soil_choice = st.selectbox("Soil Type", (["Add New"] + existing_soil) if existing_soil else ["Add New"])
        soil_type = st.text_input("Enter Soil Type") if soil_choice == "Add New" else soil_choice
        existing_root = fetch_dropdown("Trees", "root_type")
        root_choice = st.selectbox("Root Type", (["Add New"] + existing_root) if existing_root else ["Add New"])
        root_type = st.text_input("Enter Root Type") if root_choice == "Add New" else root_choice
        existing_leaf = fetch_dropdown("Trees", "leafl_type")
        leaf_choice = st.selectbox("Leaf Type", (["Add New"] + existing_leaf) if existing_leaf else ["Add New"])
        leafl_type = st.text_input("Enter Leaf Type") if leaf_choice == "Add New" else leaf_choice
        care_instructions = st.text_area("Care Instructions")
        main_photo_url = st.text_input("Main Photo URL")
        if st.button("Add Tree"):
            query = """
            INSERT INTO Trees (common_name, scientific_name, growth_rate, watering_demand, shape, care_instructions, main_photo_url, origin, soil_type, root_type, leafl_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (common_name, scientific_name, growth_rate, watering_demand, shape, care_instructions, main_photo_url, origin, soil_type, root_type, leafl_type))
            st.success("Tree added successfully!")
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Trees")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                query = """
                INSERT INTO Trees (common_name, scientific_name, growth_rate, watering_demand, shape, care_instructions, main_photo_url, origin, soil_type, root_type, leafl_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (row["common_name"], row["scientific_name"], row["growth_rate"], row["watering_demand"], row["shape"], row["care_instructions"], row["main_photo_url"], row["origin"], row["soil_type"], row["root_type"], row["leafl_type"]))
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
                common_name = st.text_input("Common Name", value=row["common_name"])
                scientific_name = st.text_input("Scientific Name", value=row["scientific_name"])
                growth_rate = st.number_input("Growth Rate (cm/yr)", value=float(row["growth_rate"]))
                watering_demand = st.text_input("Watering Demand", value=row["watering_demand"])
                shape = st.text_input("Shape", value=row["shape"])
                care_instructions = st.text_area("Care Instructions", value=row["care_instructions"])
                main_photo_url = st.text_input("Main Photo URL", value=row["main_photo_url"])
                origin = st.text_input("Origin", value=row["origin"])
                soil_type = st.text_input("Soil Type", value=row["soil_type"])
                root_type = st.text_input("Root Type", value=row["root_type"])
                leafl_type = st.text_input("Leaf Type", value=row["leafl_type"])
                if st.button("Update Tree"):
                    update_query = """
                    UPDATE Trees SET common_name=%s, scientific_name=%s, growth_rate=%s, watering_demand=%s, shape=%s, 
                    care_instructions=%s, main_photo_url=%s, origin=%s, soil_type=%s, root_type=%s, leafl_type=%s
                    WHERE tree_id=%s;
                    """
                    execute_query(update_query, (common_name, scientific_name, growth_rate, watering_demand, shape, care_instructions, main_photo_url, origin, soil_type, root_type, leafl_type, selected_id))
                    st.success("Tree updated!")

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
            for index, row in df.iterrows():
                query = """
                INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (row["nursery_name"], row["tree_common_name"], row["quantity_in_stock"], row["min_height"], row["max_height"], row["packaging_type"], row["price"], row["date"]))
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
