import streamlit as st
from handle import run_query, fetch_dataframe

def add_tree(data):
    query = """
    INSERT INTO "Trees" 
    ("Common_name", "Scientific_name", "Growth_rate", "Watering_demand", "shape", 
     "Care_instructions", "Main_Photo_url", "Origin", "Soil_type", "Root_type", "Leafl_Type")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data.get("Common_name"), data.get("Scientific_name"), data.get("Growth_rate"),
        data.get("Watering_demand"), data.get("shape"), data.get("Care_instructions"),
        data.get("Main_Photo_url"), data.get("Origin"), data.get("Soil_type"),
        data.get("Root_type"), data.get("Leafl_Type")
    )
    run_query(query, params)

def get_all_trees():
    query = 'SELECT * FROM "Trees"'
    return fetch_dataframe(query)

def tree_data_entry():
    st.subheader("Tree Data Entry (Single)")
    with st.form("tree_entry_form"):
        common_name = st.text_input("Common Name")
        scientific_name = st.text_input("Scientific Name")
        growth_rate = st.number_input("Growth Rate", min_value=0.0, format="%.2f")
        watering_demand = st.text_input("Watering Demand")
        
        # Get existing values for dropdowns if available.
        df_trees = get_all_trees()
        shapes = df_trees["shape"].dropna().unique().tolist() if not df_trees.empty else []
        shape_choice = st.selectbox("Select Existing Shape", options=[""] + shapes)
        shape = shape_choice if shape_choice != "" else st.text_input("Enter Shape")
        
        care_instructions = st.text_area("Care Instructions")
        main_photo_url = st.text_input("Main Photo URL")
        origin = st.text_input("Origin")
        soil_type = st.text_input("Soil Type")
        root_type = st.text_input("Root Type")
        # For Leafl_Type, we use the ENUM values.
        leaf_types = ['ovate', 'lanceolate', 'linear', 'Deciduous', 'Evergreen']
        leafl_type = st.selectbox("Leaf Type", options=leaf_types)
        
        submitted = st.form_submit_button("Add Tree")
        if submitted:
            data = {
                "Common_name": common_name,
                "Scientific_name": scientific_name,
                "Growth_rate": growth_rate,
                "Watering_demand": watering_demand,
                "shape": shape,
                "Care_instructions": care_instructions,
                "Main_Photo_url": main_photo_url,
                "Origin": origin,
                "Soil_type": soil_type,
                "Root_type": root_type,
                "Leafl_Type": leafl_type,
            }
            add_tree(data)
            st.success("Tree added successfully!")
