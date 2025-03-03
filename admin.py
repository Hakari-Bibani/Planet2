import streamlit as st
import sqlite3
import pandas as pd

# --- Database Connection ---
@st.cache_resource(show_spinner=False)
def get_connection():
    return sqlite3.connect("mydatabase.db", check_same_thread=False)

conn = get_connection()

# --- Helper Functions for CRUD ---
def fetch_data(table):
    return pd.read_sql_query(f"SELECT * FROM {table}", conn)

def execute_query(query, params=()):
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()

def delete_record(table, col, rec_id):
    execute_query(f"DELETE FROM {table} WHERE {col} = ?", (rec_id,))

# --- Unified function to show a combined select/input widget ---
def select_or_input(label, options):
    # If there are existing options, show a selectbox with an "Other" option;
    # then, if "Other" is selected, show a text_input.
    if options:
        choice = st.selectbox(label, options + ["Other"])
        if choice == "Other":
            choice = st.text_input(f"Enter new {label}")
    else:
        choice = st.text_input(label)
    return choice

# --- Page Layout: Sidebar with two buttons ---
page = st.sidebar.radio("Choose Function", ["Data Entry", "Search"])

st.title("Admin Panel")

if page == "Data Entry":
    st.header("Data Entry & Record Management")

    # Use tabs for the three tables
    tabs = st.tabs(["Nurseries", "Trees", "Nursery_Tree_Inventory"])

    # --- Nurseries Tab ---
    with tabs[0]:
        st.subheader("Nurseries")

        # -- Add New Nursery --
        st.markdown("#### Add New Nursery")
        with st.form("nursery_add_form"):
            reg_code = st.text_input("Registration Code")
            nursery_name = st.text_input("Nursery Name")
            address = st.text_input("Address")
            contact_name = st.text_input("Contact Name")
            contact_phone = st.text_input("Contact Phone")  # Fixed to text_input
            google_map_link = st.text_input("Google Map Link (URL)")
            additional_notes = st.text_area("Additional Notes")
            add_submit = st.form_submit_button("Add Nursery")
        if add_submit:
            execute_query("""
                INSERT INTO Nurseries 
                (Registration_code, Nursery_name, Address, Contact_name, Contact_phone, Google_map_link, Additional_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (reg_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes))
            st.success("Nursery added successfully!")

        # -- Show Existing Nurseries with Edit/Delete Options --
        st.markdown("#### Manage Existing Nurseries")
        nurseries_df = fetch_data("Nurseries")
        st.dataframe(nurseries_df)
        if not nurseries_df.empty:
            nursery_ids = nurseries_df["nursery_id"].astype(str).tolist()
            selected_nursery = st.selectbox("Select Nursery ID to Edit/Delete", [""] + nursery_ids)
            if selected_nursery:
                record = nurseries_df[nurseries_df["nursery_id"]==int(selected_nursery)].iloc[0]
                st.markdown("**Edit Nursery Record**")
                with st.form("nursery_edit_form"):
                    new_reg_code = st.text_input("Registration Code", value=record["Registration_code"])
                    new_nursery_name = st.text_input("Nursery Name", value=record["Nursery_name"])
                    new_address = st.text_input("Address", value=record["Address"])
                    new_contact_name = st.text_input("Contact Name", value=record["Contact_name"])
                    new_contact_phone = st.text_input("Contact Phone", value=str(record["Contact_phone"]))
                    new_google_map_link = st.text_input("Google Map Link (URL)", value=record["Google_map_link"])
                    new_additional_notes = st.text_area("Additional Notes", value=record["Additional_notes"])
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update"):
                            execute_query("""
                                UPDATE Nurseries SET Registration_code=?, Nursery_name=?, Address=?, Contact_name=?, Contact_phone=?, Google_map_link=?, Additional_notes=?
                                WHERE nursery_id=?
                            """, (new_reg_code, new_nursery_name, new_address, new_contact_name, new_contact_phone, new_google_map_link, new_additional_notes, record["nursery_id"]))
                            st.success("Nursery updated successfully!")
                    with col2:
                        if st.form_submit_button("Delete"):
                            delete_record("Nurseries", "nursery_id", record["nursery_id"])
                            st.success("Nursery deleted successfully!")
                            st.experimental_rerun()

    # --- Trees Tab ---
    with tabs[1]:
        st.subheader("Trees")

        # For dropdown fields, fetch distinct existing values from Trees table
        trees_df = fetch_data("Trees")
        shape_opts = trees_df["shape"].dropna().unique().tolist() if not trees_df.empty else []
        origin_opts = trees_df["Origin"].dropna().unique().tolist() if not trees_df.empty else []
        soil_opts = trees_df["Soil_type"].dropna().unique().tolist() if not trees_df.empty else []
        root_opts = trees_df["Root_type"].dropna().unique().tolist() if not trees_df.empty else []
        leaf_opts = trees_df["Leafl_Type"].dropna().unique().tolist() if not trees_df.empty else []

        # -- Add New Tree --
        st.markdown("#### Add New Tree")
        with st.form("tree_add_form"):
            common_name = st.text_input("Common Name")
            scientific_name = st.text_input("Scientific Name")
            growth_rate = st.number_input("Growth Rate (Cm/yr)", value=0.0, step=0.1)
            watering_demand = st.text_input("Watering Demand")
            shape_val = select_or_input("Shape", shape_opts)
            care_instructions = st.text_input("Care Instructions")
            main_photo_url = st.text_input("Main Photo URL")
            origin_val = select_or_input("Origin", origin_opts)
            soil_val = select_or_input("Soil Type", soil_opts)
            root_val = select_or_input("Root Type", root_opts)
            leaf_val = select_or_input("Leafl Type", leaf_opts)
            tree_add_submit = st.form_submit_button("Add Tree")
        if tree_add_submit:
            execute_query("""
                INSERT INTO Trees 
                (Common_name, Scientific_name, Growth_rate, Watering_demand, shape, Care_instructions, Main_Photo_url, Origin, Soil_type, Root_type, Leafl_Type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (common_name, scientific_name, growth_rate, watering_demand, shape_val, care_instructions, main_photo_url, origin_val, soil_val, root_val, leaf_val))
            st.success("Tree added successfully!")

        # -- Manage Existing Trees --
        st.markdown("#### Manage Existing Trees")
        trees_df = fetch_data("Trees")
        st.dataframe(trees_df)
        if not trees_df.empty:
            tree_ids = trees_df["tree_id"].astype(str).tolist()
            selected_tree = st.selectbox("Select Tree ID to Edit/Delete", [""] + tree_ids)
            if selected_tree:
                record = trees_df[trees_df["tree_id"]==int(selected_tree)].iloc[0]
                st.markdown("**Edit Tree Record**")
                with st.form("tree_edit_form"):
                    new_common_name = st.text_input("Common Name", value=record["Common_name"])
                    new_scientific_name = st.text_input("Scientific Name", value=record["Scientific_name"])
                    new_growth_rate = st.number_input("Growth Rate (Cm/yr)", value=record["Growth_rate"], step=0.1)
                    new_watering_demand = st.text_input("Watering Demand", value=record["Watering_demand"])
                    new_shape = select_or_input("Shape", shape_opts)
                    if new_shape == "":
                        new_shape = record["shape"]
                    new_care_instructions = st.text_input("Care Instructions", value=record["Care_instructions"])
                    new_main_photo_url = st.text_input("Main Photo URL", value=record["Main_Photo_url"])
                    new_origin = select_or_input("Origin", origin_opts)
                    if new_origin == "":
                        new_origin = record["Origin"]
                    new_soil = select_or_input("Soil Type", soil_opts)
                    if new_soil == "":
                        new_soil = record["Soil_type"]
                    new_root = select_or_input("Root Type", root_opts)
                    if new_root == "":
                        new_root = record["Root_type"]
                    new_leaf = select_or_input("Leafl Type", leaf_opts)
                    if new_leaf == "":
                        new_leaf = record["Leafl_Type"]
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update"):
                            execute_query("""
                                UPDATE Trees SET Common_name=?, Scientific_name=?, Growth_rate=?, Watering_demand=?, shape=?, Care_instructions=?, Main_Photo_url=?, Origin=?, Soil_type=?, Root_type=?, Leafl_Type=?
                                WHERE tree_id=?
                            """, (new_common_name, new_scientific_name, new_growth_rate, new_watering_demand, new_shape, new_care_instructions, new_main_photo_url, new_origin, new_soil, new_root, new_leaf, record["tree_id"]))
                            st.success("Tree updated successfully!")
                    with col2:
                        if st.form_submit_button("Delete"):
                            delete_record("Trees", "tree_id", record["tree_id"])
                            st.success("Tree deleted successfully!")
                            st.experimental_rerun()

    # --- Nursery_Tree_Inventory Tab ---
    with tabs[2]:
        st.subheader("Nursery Tree Inventory")

        # Get dropdown options from existing data
        nurseries_df = fetch_data("Nurseries")
        nursery_names = nurseries_df["Nursery_name"].dropna().unique().tolist() if not nurseries_df.empty else []
        trees_df = fetch_data("Trees")
        tree_common_names = trees_df["Common_name"].dropna().unique().tolist() if not trees_df.empty else []
        inv_df = fetch_data("Nursery_Tree_Inventory")
        packaging_opts = inv_df["Packaging_type"].dropna().unique().tolist() if not inv_df.empty else []

        # -- Add New Inventory Record --
        st.markdown("#### Add New Inventory Record")
        with st.form("inventory_add_form"):
            selected_nursery = st.selectbox("Nursery Name", nursery_names)
            selected_tree = st.selectbox("Tree Common Name", tree_common_names)
            quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, step=1)
            min_height = st.number_input("Minimum Height (m)", min_value=0.0, step=0.1)
            max_height = st.number_input("Maximum Height (m)", min_value=0.0, step=0.1)
            packaging_val = select_or_input("Packaging Type", packaging_opts)
            price = st.number_input("Price (IQD)", min_value=0.0, step=0.1)
            inventory_add_submit = st.form_submit_button("Add Inventory Record")
        if inventory_add_submit:
            execute_query("""
                INSERT INTO Nursery_Tree_Inventory 
                (nursery_name, "tree_common name", Quantity_in_stock, Min_height, Max_height, Packaging_type, Price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (selected_nursery, selected_tree, quantity_in_stock, min_height, max_height, packaging_val, price))
            st.success("Inventory record added successfully!")

        # -- Manage Existing Inventory Records --
        st.markdown("#### Manage Existing Inventory Records")
        inv_df = fetch_data("Nursery_Tree_Inventory")
        st.dataframe(inv_df)
        if not inv_df.empty:
            inv_ids = inv_df["tree_inventory_id"].astype(str).tolist()
            selected_inv = st.selectbox("Select Inventory ID to Edit/Delete", [""] + inv_ids)
            if selected_inv:
                record = inv_df[inv_df["tree_inventory_id"]==int(selected_inv)].iloc[0]
                st.markdown("**Edit Inventory Record**")
                with st.form("inventory_edit_form"):
                    new_nursery = st.selectbox("Nursery Name", nursery_names, index=nursery_names.index(record["nursery_name"]) if record["nursery_name"] in nursery_names else 0)
                    new_tree = st.selectbox("Tree Common Name", tree_common_names, index=tree_common_names.index(record["tree_common name"]) if record["tree_common name"] in tree_common_names else 0)
                    new_quantity = st.number_input("Quantity in Stock", min_value=0, step=1, value=record["Quantity_in_stock"])
                    new_min_height = st.number_input("Minimum Height (m)", min_value=0.0, step=0.1, value=record["Min_height"])
                    new_max_height = st.number_input("Maximum Height (m)", min_value=0.0, step=0.1, value=record["Max_height"])
                    new_packaging = select_or_input("Packaging Type", packaging_opts)
                    if new_packaging == "":
                        new_packaging = record["Packaging_type"]
                    new_price = st.number_input("Price (IQD)", min_value=0.0, step=0.1, value=record["Price"])
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update"):
                            execute_query("""
                                UPDATE Nursery_Tree_Inventory SET nursery_name=?, "tree_common name"=?, Quantity_in_stock=?, Min_height=?, Max_height=?, Packaging_type=?, Price=?
                                WHERE tree_inventory_id=?
                            """, (new_nursery, new_tree, new_quantity, new_min_height, new_max_height, new_packaging, new_price, record["tree_inventory_id"]))
                            st.success("Inventory record updated successfully!")
                    with col2:
                        if st.form_submit_button("Delete"):
                            delete_record("Nursery_Tree_Inventory", "tree_inventory_id", record["tree_inventory_id"])
                            st.success("Inventory record deleted successfully!")
                            st.experimental_rerun()

elif page == "Search":
    st.header("Search Tree Inventory")

    # Load the full inventory table
    inv_df = fetch_data("Nursery_Tree_Inventory")

    # 1. Tree Name dropdown (from "tree_common name")
    tree_names = inv_df["tree_common name"].dropna().unique().tolist() if not inv_df.empty else []
    selected_tree = st.selectbox("Tree Name", [""] + tree_names)

    # 2. Minimum Height (m) dropdown (distinct values)
    min_heights = sorted(inv_df["Min_height"].dropna().unique().tolist()) if not inv_df.empty else []
    selected_min_height = st.selectbox("Minimum Height (m)", [""] + min_heights)

    # 3. Maximum Height (m) dropdown (distinct values)
    max_heights = sorted(inv_df["Max_height"].dropna().unique().tolist()) if not inv_df.empty else []
    selected_max_height = st.selectbox("Maximum Height (m)", [""] + max_heights)

    # 4. Packaging Type dropdown
    packaging_types = inv_df["Packaging_type"].dropna().unique().tolist() if not inv_df.empty else []
    selected_packaging = st.selectbox("Packaging Type", [""] + packaging_types)

    # Construct query joining Inventory with Trees and Nurseries for additional details.
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

    st.markdown("#### Search Results")
    if result_df.empty:
        st.info("No records found for the selected criteria.")
    else:
        display_cols = [
            "Tree_Name", "Quantity_in_stock", "Scientific_name", "shape", "Watering_demand",
            "Main_Photo_url", "Origin", "Soil_type", "Root_type", "Leafl_Type", "Address",
            "Price", "Growth_rate", "Min_height", "Max_height", "Packaging_type"
        ]
        st.dataframe(result_df[display_cols])
