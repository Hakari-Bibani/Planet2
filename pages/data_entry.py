import streamlit as st
import pandas as pd
from db import run_query

def app():
    st.title("Data Entry")
    table = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory"])
    action = st.radio("Select Action", ["Single Entry", "Bulk Entry", "Update/Delete"])
    if table == "Nurseries":
        if action == "Single Entry":
            single_entry_nurseries()
        elif action == "Bulk Entry":
            bulk_entry("Nurseries")
        elif action == "Update/Delete":
            update_delete("Nurseries")
    elif table == "Trees":
        if action == "Single Entry":
            single_entry_trees()
        elif action == "Bulk Entry":
            bulk_entry("Trees")
        elif action == "Update/Delete":
            update_delete("Trees")
    elif table == "Nursery_Tree_Inventory":
        if action == "Single Entry":
            single_entry_inventory()
        elif action == "Bulk Entry":
            bulk_entry("Nursery_Tree_Inventory")
        elif action == "Update/Delete":
            update_delete("Nursery_Tree_Inventory")

def single_entry_nurseries():
    st.subheader("Add Single Nursery")
    Registration_code = st.text_input("Registration Code")
    Nursery_name = st.text_input("Nursery Name")
    Address = st.text_input("Address")
    Contact_name = st.text_input("Contact Name")
    Contact_phone = st.text_input("Contact Phone")
    Google_map_link = st.text_input("Google Map Link")
    Additional_notes = st.text_area("Additional Notes")
    if st.button("Submit Nursery"):
        query = "INSERT INTO Nurseries (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        run_query(query, (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes), fetch=False)
        st.success("Nursery added successfully")

def single_entry_trees():
    st.subheader("Add Single Tree")
    Common_name = st.text_input("Common Name")
    Scientific_name = st.text_input("Scientific Name")
    Growth_rate = st.number_input("Growth Rate (Cm/yr)", min_value=0.0, step=0.1)
    Watering_demand = st.text_input("Watering Demand")
    shapes = [row[0] for row in run_query("SELECT DISTINCT shape FROM Trees", None) if row[0]]
    shapes = shapes + ["Other"] if shapes else ["Other"]
    shape_sel = st.selectbox("Shape", shapes)
    if shape_sel == "Other":
        shape_val = st.text_input("Enter new Shape")
    else:
        shape_val = shape_sel
    care = st.text_area("Care Instructions")
    Main_Photo_url = st.text_input("Main Photo URL")
    origins = [row[0] for row in run_query("SELECT DISTINCT Origin FROM Trees", None) if row[0]]
    origins = origins + ["Other"] if origins else ["Other"]
    origin_sel = st.selectbox("Origin", origins)
    if origin_sel == "Other":
        origin_val = st.text_input("Enter new Origin")
    else:
        origin_val = origin_sel
    soils = [row[0] for row in run_query("SELECT DISTINCT Soil_type FROM Trees", None) if row[0]]
    soils = soils + ["Other"] if soils else ["Other"]
    soil_sel = st.selectbox("Soil Type", soils)
    if soil_sel == "Other":
        soil_val = st.text_input("Enter new Soil Type")
    else:
        soil_val = soil_sel
    roots = [row[0] for row in run_query("SELECT DISTINCT Root_type FROM Trees", None) if row[0]]
    roots = roots + ["Other"] if roots else ["Other"]
    root_sel = st.selectbox("Root Type", roots)
    if root_sel == "Other":
        root_val = st.text_input("Enter new Root Type")
    else:
        root_val = root_sel
    leafs = [row[0] for row in run_query("SELECT DISTINCT Leafl_Type FROM Trees", None) if row[0]]
    leafs = leafs + ["Other"] if leafs else ["Other"]
    leaf_sel = st.selectbox("Leaf Type", leafs)
    if leaf_sel == "Other":
        leaf_val = st.text_input("Enter new Leaf Type")
    else:
        leaf_val = leaf_sel
    if st.button("Submit Tree"):
        query = "INSERT INTO Trees (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        run_query(query, (Common_name, Scientific_name, Growth_rate, Watering_demand, shape_val, care, Main_Photo_url, origin_val, soil_val, root_val, leaf_val), fetch=False)
        st.success("Tree added successfully")

def single_entry_inventory():
    st.subheader("Add Single Nursery Tree Inventory")
    nurseries = [row[0] for row in run_query("SELECT Nursery_name FROM Nurseries", None)]
    nursery_sel = st.selectbox("Nursery Name", nurseries)
    trees = [row[0] for row in run_query("SELECT Common_name FROM Trees", None)]
    tree_sel = st.selectbox("Tree Common Name", trees)
    Quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1)
    Min_height = st.number_input("Min Height", min_value=0.0, step=0.1)
    Max_height = st.number_input("Max Height", min_value=0.0, step=0.1)
    packaging_types = [row[0] for row in run_query("SELECT DISTINCT Packaging_type FROM Nursery_Tree_Inventory", None) if row[0]]
    packaging_types = packaging_types + ["Other"] if packaging_types else ["Other"]
    packaging_sel = st.selectbox("Packaging Type", packaging_types)
    if packaging_sel == "Other":
        packaging_val = st.text_input("Enter new Packaging Type")
    else:
        packaging_val = packaging_sel
    Price = st.number_input("Price (IQD)", min_value=0.0, step=0.1)
    Date = st.date_input("Date")
    if st.button("Submit Inventory"):
        query = "INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        run_query(query, (nursery_sel, tree_sel, Quantity_in_stock, Min_height, Max_height, packaging_val, Price, Date), fetch=False)
        st.success("Inventory record added successfully")

def bulk_entry(table):
    st.subheader(f"Bulk Entry for {table}")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
        st.dataframe(df)
        if st.button("Submit Bulk Data"):
            if table == "Nurseries":
                for _, row in df.iterrows():
                    query = "INSERT INTO Nurseries (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    run_query(query, (row['Registration_code'], row['Nursery_name'], row['Address'], row['Contact_name'], row['Contact_phone'], row['Google_map_link'], row['Additional_notes']), fetch=False)
            elif table == "Trees":
                for _, row in df.iterrows():
                    query = "INSERT INTO Trees (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    run_query(query, (row['Common_name'], row['Scientific_name'], row['Growth_rate'], row['Watering_demand'], row['shape'], row['Care_instructions'], row['Main_Photo_url'], row['Origin'], row['Soil_type'], row['Root_type'], row['Leafl_Type']), fetch=False)
            elif table == "Nursery_Tree_Inventory":
                for _, row in df.iterrows():
                    query = "INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    run_query(query, (row['nursery_name'], row['tree_common_name'], row['Quantity_in_stock'], row['Min_height'], row['Max_height'], row['Packaging_type'], row['Price'], row['Date']), fetch=False)
            st.success("Bulk data added successfully")

def update_delete(table):
    st.subheader(f"Update/Delete for {table}")
    if table == "Nurseries":
        data = run_query("SELECT nursery_id, Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes FROM Nurseries")
    elif table == "Trees":
        data = run_query("SELECT tree_id, Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type FROM Trees")
    elif table == "Nursery_Tree_Inventory":
        data = run_query("SELECT tree_inventory_id, nursery_name, tree_common_name, Quantity_in_stock, Min_height, Max_height, Packaging_type, Price, Date FROM Nursery_Tree_Inventory")
    df = pd.DataFrame(data)
    st.dataframe(df)
    record_id = st.text_input("Enter the ID of the record to update/delete")
    if st.button("Delete Record"):
        if table == "Nurseries":
            query = "DELETE FROM Nurseries WHERE nursery_id = %s"
        elif table == "Trees":
            query = "DELETE FROM Trees WHERE tree_id = %s"
        elif table == "Nursery_Tree_Inventory":
            query = "DELETE FROM Nursery_Tree_Inventory WHERE tree_inventory_id = %s"
        run_query(query, (record_id,), fetch=False)
        st.success("Record deleted")
    st.write("Update Record:")
    updated_values = st.text_area("Enter new values as comma separated (order as in table columns excluding ID)")
    if st.button("Update Record"):
        if table == "Nurseries":
            query = "UPDATE Nurseries SET Registration_code = %s, Nursery_name = %s, Address = %s, Contact_name = %s, Contact_phone = %s, Google_map_link = %s, Additional_notes = %s WHERE nursery_id = %s"
        elif table == "Trees":
            query = "UPDATE Trees SET Common_name = %s, Scientific_name = %s, Growth_rate = %s, Watering_demand = %s, shape = %s, Care_instructions = %s, Main_Photo_url = %s, Origin = %s, Soil_type = %s, Root_type = %s, Leafl_Type = %s WHERE tree_id = %s"
        elif table == "Nursery_Tree_Inventory":
            query = "UPDATE Nursery_Tree_Inventory SET nursery_name = %s, tree_common_name = %s, Quantity_in_stock = %s, Min_height = %s, Max_height = %s, Packaging_type = %s, Price = %s, Date = %s WHERE tree_inventory_id = %s"
        values = [x.strip() for x in updated_values.split(",")]
        values.append(record_id)
        run_query(query, tuple(values), fetch=False)
        st.success("Record updated")
