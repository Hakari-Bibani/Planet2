import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

# Custom CSS for improved styling
def local_css():
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )

def handle_inventory(entry_type):
    """
    Handles Single Entry, Bulk Entry, and Modify/Delete for Nursery_Tree_Inventory.
    """

    # Styling for form headers
    st.markdown(
        f"<h2 style='color: #2c3e50; text-align: center;'>{entry_type} Form</h2>", 
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------------
    # SINGLE ENTRY
    # -------------------------------------------------------------------
    if entry_type == "Single Entry":
        st.subheader("Add Single Nursery Tree Inventory")

        # Two-column layout for input fields
        col1, col2 = st.columns(2)

        with col1:
            # Fetch nursery names
            nursery_query = "SELECT nursery_name FROM Nurseries;"
            nurseries_list = [row["nursery_name"] for row in run_query(nursery_query) or []]
            nursery_name = st.selectbox("🏡 Nursery Name", nurseries_list, key="single_nursery")

            # Fetch tree names
            tree_query = "SELECT common_name FROM Trees;"
            tree_names = [row["common_name"] for row in run_query(tree_query) or []]
            tree_common_name = st.selectbox("🌳 Tree Common Name", tree_names, key="single_tree")

            quantity_in_stock = st.number_input("📦 Quantity in Stock", min_value=0, step=1, key="single_quantity")

        with col2:
            min_height = st.number_input("📏 Minimum Height", value=0.0, key="single_min_height")
            max_height = st.number_input("📏 Maximum Height", value=0.0, key="single_max_height")

            packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
            packaging_choice = st.selectbox(
                "📦 Packaging Type",
                (["Add New"] + packaging_types) if packaging_types else ["Add New"],
                key="single_packaging_choice"
            )
            # If user chooses "Add New", show a text input for the new packaging type
            packaging_type = (
                st.text_input("Enter Packaging Type", key="single_packaging_new")
                if packaging_choice == "Add New" 
                else packaging_choice
            )

            price = st.number_input("💰 Price (IQD)", value=0.0, key="single_price")
            date = st.date_input("📅 Date", key="single_date")

        # Insert into DB when button is pressed
        if st.button("📥 Add Inventory Record", key="single_add_button"):
            query = """
                INSERT INTO Nursery_Tree_Inventory 
                    (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(
                query,
                (
                    nursery_name,
                    tree_common_name,
                    quantity_in_stock,
                    min_height,
                    max_height,
                    packaging_type,
                    price,
                    date
                )
            )
            st.success("✅ Inventory record added!")

    # -------------------------------------------------------------------
    # BULK ENTRY
    # -------------------------------------------------------------------
    elif entry_type == "Bulk Entry":
        st.subheader("Bulk Add Nursery Tree Inventory")
        st.markdown(
            """
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3>📄 Bulk Inventory Upload</h3>
            <p>Upload a CSV file with inventory details. 
               Ensure columns match: 
               <b>nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date</b>
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        file = st.file_uploader(
            "📁 Upload CSV", 
            type=["csv"], 
            help="CSV file with inventory details",
            key="bulk_file_uploader"
        )
        if file is not None:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()  # ensure headers are lower-case

            # Show a preview of uploaded data
            st.write("📋 Preview of Uploaded Data:")
            st.dataframe(df)

            if st.button("📂 Confirm Bulk Upload", key="bulk_upload_button"):
                for _, row in df.iterrows():
                    query = """
                        INSERT INTO Nursery_Tree_Inventory 
                            (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    execute_query(
                        query,
                        (
                            row["nursery_name"],
                            row["tree_common_name"],
                            row["quantity_in_stock"],
                            row["min_height"],
                            row["max_height"],
                            row["packaging_type"],
                            row["price"],
                            row["date"]
                        )
                    )
                st.success("✅ Bulk inventory records added!")

    # -------------------------------------------------------------------
    # MODIFY/DELETE
    # -------------------------------------------------------------------
    elif entry_type == "Modify/Delete":
        st.subheader("Modify/Delete Nursery Tree Inventory")

        query = "SELECT * FROM Nursery_Tree_Inventory;"
        data = run_query(query)

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            st.markdown(
                """
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <h3>🌳 Inventory Management</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Create tabs for Modify / Delete
            selected_id = st.selectbox("📦 Select Inventory ID", df["tree_inventory_id"], key="modify_inventory_id")
            action_tabs = st.tabs(["Modify", "Delete"])

            # -----------------------
            # Modify Tab
            # -----------------------
            with action_tabs[0]:
                row = df[df["tree_inventory_id"] == selected_id].iloc[0]

                # Two-column layout
                col1, col2 = st.columns(2)

                with col1:
                    # Re-fetch nursery and tree names for the dropdowns
                    nursery_query = "SELECT nursery_name FROM Nurseries;"
                    nursery_list = [r["nursery_name"] for r in run_query(nursery_query) or []]
                    # Pre-select the existing nursery_name if it's in the list
                    if row["nursery_name"] in nursery_list:
                        default_nursery_idx = nursery_list.index(row["nursery_name"])
                    else:
                        default_nursery_idx = 0
                    nursery_name = st.selectbox("🏡 Nursery Name", nursery_list, index=default_nursery_idx, key="modify_nursery_name")

                    tree_query = "SELECT common_name FROM Trees;"
                    tree_names = [r["common_name"] for r in run_query(tree_query) or []]
                    if row["tree_common_name"] in tree_names:
                        default_tree_idx = tree_names.index(row["tree_common_name"])
                    else:
                        default_tree_idx = 0
                    tree_common_name = st.selectbox("🌳 Tree Common Name", tree_names, index=default_tree_idx, key="modify_tree_common_name")

                    quantity_in_stock = st.number_input("📦 Quantity in Stock", min_value=0, step=1, value=int(row["quantity_in_stock"]), key="modify_quantity")

                with col2:
                    min_height = st.number_input("📏 Minimum Height", value=float(row["min_height"]), key="modify_min_height")
                    max_height = st.number_input("📏 Maximum Height", value=float(row["max_height"]), key="modify_max_height")

                    packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
                    packaging_choice = st.selectbox(
                        "📦 Packaging Type", 
                        (["Add New"] + packaging_types) if packaging_types else ["Add New"], 
                        index=0,
                        key="modify_packaging_choice"
                    )
                    packaging_type = (
                        st.text_input("Enter Packaging Type", value=row["packaging_type"], key="modify_packaging_type")
                        if packaging_choice == "Add New"
                        else packaging_choice
                    )

                    price = st.number_input("💰 Price (IQD)", value=float(row["price"]), key="modify_price")
                    date = st.date_input("📅 Date", value=pd.to_datetime(row["date"]), key="modify_date")

                if st.button("💾 Update Inventory Record", key="modify_update_button"):
                    update_query = """
                        UPDATE Nursery_Tree_Inventory 
                        SET 
                            nursery_name=%s,
                            tree_common_name=%s,
                            quantity_in_stock=%s,
                            min_height=%s,
                            max_height=%s,
                            packaging_type=%s,
                            price=%s,
                            date=%s
                        WHERE tree_inventory_id=%s;
                    """
                    execute_query(
                        update_query,
                        (
                            nursery_name, 
                            tree_common_name, 
                            quantity_in_stock, 
                            min_height, 
                            max_height, 
                            packaging_type, 
                            price, 
                            date, 
                            selected_id
                        )
                    )
                    st.success("✅ Inventory record updated!")

            # -----------------------
            # Delete Tab
            # -----------------------
            with action_tabs[1]:
                if st.button("🗑️ Confirm Delete", key="delete_button"):
                    delete_query = "DELETE FROM Nursery_Tree_Inventory WHERE tree_inventory_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("🗑️ Inventory record deleted!")

        else:
            st.info("ℹ️ No inventory data available.")

def main():
    local_css()
    st.markdown(
        "<h1 style='text-align: center; color: #2c3e50;'>🌳 Nursery Tree Inventory Management System</h1>",
        unsafe_allow_html=True
    )

    tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])

    with tabs[0]:
        handle_inventory("Single Entry")
    with tabs[1]:
        handle_inventory("Bulk Entry")
    with tabs[2]:
        handle_inventory("Modify/Delete")

if __name__ == "__main__":
    main()
