import streamlit as st
import pandas as pd
import sqlite3

#############################
# Database connection & caching
#############################

@st.cache_resource(show_spinner=False)
def get_connection():
    # Connect to SQLite database; ensure the file is in the app directory.
    conn = sqlite3.connect("mydatabase.db", check_same_thread=False)
    return conn

# Cache table data to reduce repeated queries; clear cache after data modifications.
@st.cache_data(show_spinner=False)
def get_table_df(table_name: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return df

def clear_cache():
    get_table_df.clear()

#############################
# Sidebar Navigation
#############################

st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Search", "Data Entry"])

#############################
# Data Entry Page
#############################
if page == "Data Entry":
    st.title("Data Entry and Management")
    st.info("Use the tabs below to add, edit, modify, delete single records or upload bulk CSV data.")
    
    # Three tabs for three tables.
    tab1, tab2, tab3 = st.tabs(["Nurseries", "Trees", "Nursery Tree Inventory"])
    
    ###############
    # Nurseries Tab
    ###############
    with tab1:
        st.subheader("Manage Nurseries")
        st.write("### Bulk Upload")
        nursery_csv = st.file_uploader("Upload CSV to add Nurseries", type=["csv"], key="nursery_csv")
        if nursery_csv is not None:
            try:
                new_nurseries = pd.read_csv(nursery_csv)
                conn = get_connection()
                new_nurseries.to_sql("Nurseries", conn, if_exists="append", index=False)
                clear_cache()
                st.success(f"Added {len(new_nurseries)} new nursery records.")
            except Exception as e:
                st.error(f"Error uploading CSV: {e}")
        
        st.write("### Edit / Add / Delete Data")
        nurseries_df = get_table_df("Nurseries")
        # Display inline editable table. The Contact Phone field is taken as text.
        edited_nurseries = st.data_editor(
            nurseries_df,
            num_rows="dynamic",
            hide_index=True,
            key="nurseries_editor"
        )
        if st.button("Save Nurseries"):
            try:
                conn = get_connection()
                # Overwrite the table with the edited DataFrame.
                edited_nurseries.to_sql("Nurseries", conn, if_exists="replace", index=False)
                clear_cache()
                st.success("Nurseries table updated successfully.")
            except Exception as e:
                st.error(f"Error saving data: {e}")
    
    ###############
    # Trees Tab
    ###############
    with tab2:
        st.subheader("Manage Trees")
        st.write("### Bulk Upload")
        trees_csv = st.file_uploader("Upload CSV to add Trees", type=["csv"], key="trees_csv")
        if trees_csv is not None:
            try:
                new_trees = pd.read_csv(trees_csv)
                conn = get_connection()
                new_trees.to_sql("Trees", conn, if_exists="append", index=False)
                clear_cache()
                st.success(f"Added {len(new_trees)} new tree records.")
            except Exception as e:
                st.error(f"Error uploading CSV: {e}")
        
        st.write("### Edit / Add / Delete Data")
        trees_df = get_table_df("Trees")
        # For dropdowns that allow both selection and new input, we set these columns as categories.
        for col in ["shape", "Origin", "Soil_type", "Root_type", "Leafl_Type"]:
            if col in trees_df.columns:
                existing = trees_df[col].dropna().unique().tolist()
                trees_df[col] = pd.Categorical(trees_df[col], categories=existing)
        edited_trees = st.data_editor(
            trees_df,
            num_rows="dynamic",
            hide_index=True,
            key="trees_editor"
        )
        if st.button("Save Trees"):
            try:
                conn = get_connection()
                edited_trees.to_sql("Trees", conn, if_exists="replace", index=False)
                clear_cache()
                st.success("Trees table updated successfully.")
            except Exception as e:
                st.error(f"Error saving data: {e}")
    
    #############################
    # Nursery Tree Inventory Tab
    #############################
    with tab3:
        st.subheader("Manage Nursery Tree Inventory")
        st.write("### Bulk Upload")
        inv_csv = st.file_uploader("Upload CSV to add Inventory records", type=["csv"], key="inv_csv")
        if inv_csv is not None:
            try:
                new_inv = pd.read_csv(inv_csv)
                conn = get_connection()
                new_inv.to_sql("Nursery_Tree_Inventory", conn, if_exists="append", index=False)
                clear_cache()
                st.success(f"Added {len(new_inv)} new inventory records.")
            except Exception as e:
                st.error(f"Error uploading CSV: {e}")
        
        st.write("### Edit / Add / Delete Data")
        inv_df = get_table_df("Nursery_Tree_Inventory")
        # For Packaging_type, use dropdown behavior.
        if "Packaging_type" in inv_df.columns:
            existing_pack = inv_df["Packaging_type"].dropna().unique().tolist()
            inv_df["Packaging_type"] = pd.Categorical(inv_df["Packaging_type"], categories=existing_pack)
        # For foreign key fields: Nursery_name & tree_common_name, populate from other tables.
        nurseries = get_table_df("Nurseries")["Nursery_name"].dropna().unique().tolist()
        if "Nursery_name" in inv_df.columns:
            inv_df["Nursery_name"] = pd.Categorical(inv_df["Nursery_name"], categories=nurseries)
        trees = get_table_df("Trees")["Common_name"].dropna().unique().tolist()
        # We assume the inventory table uses "tree_common_name" as the column name.
        if "tree_common_name" in inv_df.columns:
            inv_df["tree_common_name"] = pd.Categorical(inv_df["tree_common_name"], categories=trees)
        edited_inv = st.data_editor(
            inv_df,
            num_rows="dynamic",
            hide_index=True,
            key="inv_editor"
        )
        if st.button("Save Inventory"):
            try:
                conn = get_connection()
                edited_inv.to_sql("Nursery_Tree_Inventory", conn, if_exists="replace", index=False)
                clear_cache()
                st.success("Inventory table updated successfully.")
            except Exception as e:
                st.error(f"Error saving data: {e}")

#############################
# Search Page
#############################
elif page == "Search":
    st.title("Search Trees in Nurseries")
    
    # Retrieve distinct filter options from the inventory table.
    inv_df = get_table_df("Nursery_Tree_Inventory")
    tree_names = ["All"] + sorted(inv_df["tree_common_name"].dropna().unique().tolist())
    min_heights = ["All"] + sorted([str(x) for x in inv_df["Min_height"].dropna().unique().tolist()])
    max_heights = ["All"] + sorted([str(x) for x in inv_df["Max_height"].dropna().unique().tolist()])
    packaging_types = ["All"] + sorted(inv_df["Packaging_type"].dropna().unique().tolist())
    
    st.write("### Filter Criteria")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        tree_filter = st.selectbox("Tree Name", tree_names)
    with col2:
        min_filter = st.selectbox("Minimum Height (m)", min_heights)
    with col3:
        max_filter = st.selectbox("Maximum Height (m)", max_heights)
    with col4:
        pack_filter = st.selectbox("Packaging Type", packaging_types)
    
    # Build a dynamic SQL query based on selected filters.
    query = """
        SELECT inv.Quantity_in_stock,
               t.Scientific_name,
               t.shape,
               t.Watering_demand,
               t.Main_Photo_url,
               t.Origin,
               t.Soil_type,
               t.Root_type,
               t.Leafl_Type,
               n.Address,
               inv.Price,
               t.Growth_rate
        FROM Nursery_Tree_Inventory AS inv
        JOIN Trees AS t ON inv.tree_common_name = t.Common_name
        JOIN Nurseries AS n ON inv.Nursery_name = n.Nursery_name
        WHERE 1=1
    """
    filters = []
    if tree_filter != "All":
        filters.append(f"inv.tree_common_name = '{tree_filter}'")
    if min_filter != "All":
        filters.append(f"inv.Min_height = {min_filter}")
    if max_filter != "All":
        filters.append(f"inv.Max_height = {max_filter}")
    if pack_filter != "All":
        filters.append(f"inv.Packaging_type = '{pack_filter}'")
    if filters:
        query += " AND " + " AND ".join(filters)
    
    conn = get_connection()
    try:
        results_df = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error fetching search results: {e}")
        results_df = pd.DataFrame()
    
    st.write("### Search Results")
    if results_df.empty:
        st.info("No records found for the selected criteria.")
    else:
        st.dataframe(results_df, use_container_width=True)
