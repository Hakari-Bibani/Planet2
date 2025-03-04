import streamlit as st
from handle import fetch_dataframe

def search_inventory(tree_name=None, min_height=None, max_height=None, packaging_type=None):
    base_query = """
    SELECT nti.*, 
           t."Scientific_name", t."Growth_rate", t."shape" as tree_shape, 
           t."Watering_demand", t."Main_Photo_url", t."Origin", t."Soil_type", 
           t."Root_type", t."Leafl_Type", n."Address"
    FROM "Nursery_Tree_Inventory" nti
    LEFT JOIN "Trees" t ON nti."tree_common_name" = t."Common_name"
    LEFT JOIN "Nurseries" n ON nti."nursery_name" = n."Nursery_name"
    WHERE 1=1
    """
    conditions = []
    params = []
    if tree_name:
        conditions.append(' nti."tree_common_name" = %s ')
        params.append(tree_name)
    if min_height is not None:
        conditions.append(' nti."Min_height" >= %s ')
        params.append(min_height)
    if max_height is not None:
        conditions.append(' nti."Max_height" <= %s ')
        params.append(max_height)
    if packaging_type:
        conditions.append(' nti."Packaging_type" = %s ')
        params.append(packaging_type)
    
    if conditions:
        query = base_query + " AND " + " AND ".join(conditions)
    else:
        query = base_query
    
    return fetch_dataframe(query, params)

def search_page():
    st.subheader("Search Nursery Tree Inventory")
    
    # Fetch dropdown values from the Nursery_Tree_Inventory table
    from Nursery_Tree_Inventory import get_all_inventory
    df_inventory = get_all_inventory()
    if df_inventory.empty:
        st.info("No inventory data available.")
        return

    tree_names = df_inventory["tree_common_name"].unique().tolist()
    packaging_types = df_inventory["Packaging_type"].unique().tolist()
    
    # For the height ranges, use min and max values from the data if available.
    min_height_val = float(df_inventory["Min_height"].min()) if not df_inventory["Min_height"].isnull().all() else 0.0
    max_height_val = float(df_inventory["Max_height"].max()) if not df_inventory["Max_height"].isnull().all() else 10.0
    
    tree_name = st.selectbox("Tree Name", options=[""] + tree_names)
    min_height = st.slider("Minimum Height (m)", min_value=min_height_val, max_value=max_height_val, value=min_height_val)
    max_height = st.slider("Maximum Height (m)", min_value=min_height_val, max_value=max_height_val, value=max_height_val)
    packaging_type = st.selectbox("Packaging Type", options=[""] + packaging_types)
    
    if st.button("Search"):
        result_df = search_inventory(
            tree_name=tree_name if tree_name != "" else None,
            min_height=min_height,
            max_height=max_height,
            packaging_type=packaging_type if packaging_type != "" else None,
        )
        st.dataframe(result_df)
