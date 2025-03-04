import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

def local_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        margin: 0 5px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e6e9ef;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 6px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

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
            df.columns = df.columns.str.lower()  # ensure headers are lower-case
            for index, row in df.iterrows():
                query = """
                INSERT INTO Trees (common_name, scientific_name, growth_rate, watering_demand, shape, care_instructions, main_photo_url, origin, soil_type, root_type, leafl_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                execute_query(query, (
                    row["common_name"],
                    row["scientific_name"],
                    row["growth_rate"],
                    row["watering_demand"],
                    row["shape"],
                    row["care_instructions"],
                    row["main_photo_url"],
                    row["origin"],
                    row["soil_type"],
                    row["root_type"],
                    row["leafl_type"]
                ))
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

def main():
    local_css()
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🌳 Tree Management System</h1>", unsafe_allow_html=True)
    
    # Create horizontal tabs for the entry types
    tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])
    
    with tabs[0]:
        handle_trees("Single Entry")
    with tabs[1]:
        handle_trees("Bulk Entry")
    with tabs[2]:
        handle_trees("Modify/Delete")

if __name__ == "__main__":
    main()
