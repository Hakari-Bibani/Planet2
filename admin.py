import streamlit as st
import sqlite3
import pandas as pd

# Function to get database connection
def get_connection():
    return sqlite3.connect("mydatabase.db", check_same_thread=False)

conn = get_connection()
st.title("Admin Panel - Data Entry and Management")

# Sidebar navigation for different tables
table_option = st.sidebar.selectbox("Select Table", 
    ["Nurseries", "Trees", "Nursery_Tree_Inventory"])

# --------------------------
# 1. Nurseries Section
# --------------------------
if table_option == "Nurseries":
    st.header("Nurseries Data Entry")
    st.subheader("Add Single Nursery Record")
    with st.form("nursery_form"):
        reg_code = st.text_input("Registration Code")
        nursery_name = st.text_input("Nursery Name")
        address = st.text_input("Address")
        contact_name = st.text_input("Contact Name")
        contact_phone = st.number_input("Contact Phone", step=1, format="%d")
        google_map_link = st.text_input("Google Map Link (URL)")
        additional_notes = st.text_area("Additional Notes")
        submit_nursery = st.form_submit_button("Add Nursery")
    if submit_nursery:
        conn.execute("""
            INSERT INTO Nurseries 
            (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (reg_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes))
        conn.commit()
        st.success("Nursery added successfully!")

    st.subheader("Existing Nurseries")
    nurseries_df = pd.read_sql_query("SELECT * FROM Nurseries", conn)
    st.dataframe(nurseries_df)
    # (Optional: add options to update or delete a row here)

# --------------------------
# 2. Trees Section
# --------------------------
elif table_option == "Trees":
    st.header("Trees Data Entry")
    st.subheader("Add Single Tree Record")
    
    # Retrieve distinct values for dropdown fields from existing Trees records
    trees_dropdown_df = pd.read_sql_query(
        "SELECT DISTINCT shape, Origin, Soil_type, Root_type, Leafl_Type FROM Trees", conn)
    
    # Prepare dropdown lists (add "Add New" option)
    def dropdown_list(col):
        items = trees_dropdown_df[col].dropna().unique().tolist() if not trees_dropdown_df.empty else []
        return items + ["Add New"]
    
    shape_options = dropdown_list("shape")
    origin_options = dropdown_list("Origin")
    soil_options = dropdown_list("Soil_type")
    root_options = dropdown_list("Root_type")
    leaf_options = dropdown_list("Leafl_Type")
    
    with st.form("trees_form"):
        common_name = st.text_input("Common Name")
        scientific_name = st.text_input("Scientific Name")
        growth_rate = st.number_input("Growth Rate (Cm/yr)", value=0.0, step=0.1)
        watering_demand = st.text_input("Watering Demand")
        
        shape_choice = st.selectbox("Shape", options=shape_options)
        if shape_choice == "Add New":
            shape_choice = st.text_input("Enter New Shape")
            
        care_instructions = st.text_input("Care Instructions")
        main_photo_url = st.text_input("Main Photo URL")
        
        origin_choice = st.selectbox("Origin", options=origin_options)
        if origin_choice == "Add New":
            origin_choice = st.text_input("Enter New Origin")
            
        soil_choice = st.selectbox("Soil Type", options=soil_options)
        if soil_choice == "Add New":
            soil_choice = st.text_input("Enter New Soil Type")
            
        root_choice = st.selectbox("Root Type", options=root_options)
        if root_choice == "Add New":
            root_choice = st.text_input("Enter New Root Type")
            
        leaf_choice = st.selectbox("Leafl Type", options=leaf_options)
        if leaf_choice == "Add New":
            leaf_choice = st.text_input("Enter New Leafl Type")
            
        submit_tree = st.form_submit_button("Add Tree")
    if submit_tree:
        conn.execute("""
            INSERT INTO Trees 
            (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (common_name, scientific_name, growth_rate, watering_demand, shape_choice, care_instructions, main_photo_url, origin_choice, soil_choice, root_choice, leaf_choice))
        conn.commit()
        st.success("Tree added successfully!")
        
    st.subheader("Existing Trees")
    trees_df = pd.read_sql_query("SELECT * FROM Trees", conn)
    st.dataframe(trees_df)
    # (Optional: add options to update or delete a row here)

# --------------------------
# 3. Nursery_Tree_Inventory Section
# --------------------------
elif table_option == "Nursery_Tree_Inventory":
    st.header("Nursery Tree Inventory Data Entry")
    st.subheader("Add Single Inventory Record")
    
    # Dropdown for nursery_name from Nurseries
    nurseries_df = pd.read_sql_query("SELECT Nursery_name FROM Nurseries", conn)
    nursery_names = nurseries_df["Nursery_name"].dropna().unique().tolist() if not nurseries_df.empty else []
    
    # Dropdown for tree_common name from Trees (Common_name)
    trees_df = pd.read_sql_query("SELECT Common_name FROM Trees", conn)
    tree_common_names = trees_df["Common_name"].dropna().unique().tolist() if not trees_df.empty else []
    
    # Dropdown for Packaging_type from existing Nursery_Tree_Inventory
    packaging_df = pd.read_sql_query("SELECT DISTINCT Packaging_type FROM Nursery_Tree_Inventory", conn)
    packaging_types = packaging_df["Packaging_type"].dropna().unique().tolist() if not packaging_df.empty else []
    
    with st.form("inventory_form"):
        selected_nursery = st.selectbox("Nursery Name", options=nursery_names)
        selected_tree = st.selectbox("Tree Common Name", options=tree_common_names)
        quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1)
        min_height = st.number_input("Minimum Height (m)", min_value=0.0, step=0.1)
        max_height = st.number_input("Maximum Height (m)", min_value=0.0, step=0.1)
        packaging_choice = st.selectbox("Packaging Type", options=packaging_types + ["Add New"])
        if packaging_choice == "Add New":
            packaging_choice = st.text_input("Enter New Packaging Type")
        price = st.number_input("Price (IQD)", min_value=0.0, step=0.1)
        submit_inventory = st.form_submit_button("Add Inventory Record")
    if submit_inventory:
        conn.execute("""
            INSERT INTO Nursery_Tree_Inventory 
            (nursery_name, "tree_common name", Quantity_in_stock, Min_height, Max_height, Packaging_type, Price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (selected_nursery, selected_tree, quantity_in_stock, min_height, max_height, packaging_choice, price))
        conn.commit()
        st.success("Inventory record added successfully!")
        
    st.subheader("Existing Inventory Records")
    inventory_df = pd.read_sql_query("SELECT * FROM Nursery_Tree_Inventory", conn)
    st.dataframe(inventory_df)
    # (Optional: add options to update or delete a row here)

