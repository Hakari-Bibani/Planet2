import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

# Custom CSS for improved styling
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

def handle_inventory(entry_type):
    # Styling for form headers
    st.markdown(f"<h2 style='color: #2c3e50; text-align: center;'>{entry_type} Form</h2>", unsafe_allow_html=True)

    if entry_type == "Single Entry":
        col1, col2 = st.columns(2)
        
        with col1:
            nursery_query = "SELECT nursery_name FROM Nurseries;"
            nurseries = [row["nursery_name"] for row in run_query(nursery_query) or []]
            nursery_name = st.selectbox("🏡 Nursery Name", nurseries)
            tree_query = "SELECT common_name FROM Trees;"
            tree_names = [row["common_name"] for row in run_query(tree_query) or []]
            tree_common_name = st.selectbox("🌳 Tree Common Name", tree_names)
            quantity_in_stock = st.number_input("📦 Quantity in Stock", min_value=0, step=1)
        
        with col2:
            min_height = st.number_input("📏 Minimum Height", value=0.0)
            max_height = st.number_input("📏 Maximum Height", value=0.0)
            packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
            packaging_choice = st.selectbox("📦 Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"])
            packaging_type = st.text_input("Enter Packaging Type") if packaging_choice == "Add New" else packaging_choice
            price = st.number_input("💰 Price (IQD)", value=0.0)
            date = st.date_input("📅 Date")
        
        if st.button("📥 Add Inventory Record"):
            query = """
            INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            execute_query(query, (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date))
            st.success("✅ Inventory record added!")

    elif entry_type == "Bulk Entry":
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3>📄 Bulk Inventory Upload</h3>
        <p>Upload a CSV file with inventory details. Ensure columns match: nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date</p>
        </div>
        """, unsafe_allow_html=True)
        
        file = st.file_uploader("📁 Upload CSV", type=["csv"], help="CSV file with inventory details")
        if file is not None:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()  # ensure headers are lower-case
            
            st.write("📋 Preview of Uploaded Data:")
            st.dataframe(df)
            
            if st.button("📂 Confirm Bulk Upload"):
                for index, row in df.iterrows():
                    query = """
                    INSERT INTO Nursery_Tree_Inventory (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    execute_query(query, (
                        row["nursery_name"],
                        row["tree_common_name"],
                        row["quantity_in_stock"],
                        row["min_height"],
                        row["max_height"],
                        row["packaging_type"],
                        row["price"],
                        row["date"]
                    ))
                st.success("✅ Bulk inventory records added!")

    elif entry_type == "Modify/Delete":
        query = "SELECT * FROM Nursery_Tree_Inventory;"
        data = run_query(query)
        
        if data:
            df = pd.DataFrame(data)
            
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
            <h3>🌳 Inventory Management</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(df, use_container_width=True)
            
            selected_id = st.selectbox("📦 Select Inventory ID to Modify/Delete", df["tree_inventory_id"])
            action_tabs = st.tabs(["Modify", "Delete"])
            
            with action_tabs[0]:
                row = df[df["tree_inventory_id"] == selected_id].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nursery_query = "SELECT nursery_name FROM Nurseries;"
                    nurseries = [r["nursery_name"] for r in run_query(nursery_query) or []]
                    nursery_name = st.selectbox("🏡 Nursery Name", nurseries, index=nurseries.index(row["nursery_name"]) if row["nursery_name"] in nurseries else 0)
                    tree_query = "SELECT common_name FROM Trees;"
                    tree_names = [r["common_name"] for r in run_query(tree_query) or []]
                    tree_common_name = st.selectbox("🌳 Tree Common Name", tree_names, index=tree_names.index(row["tree_common_name"]) if row["tree_common_name"] in tree_names else 0)
                    quantity_in_stock = st.number_input("📦 Quantity in Stock", min_value=0, step=1, value=row["quantity_in_stock"])
                
                with col2:
                    min_height = st.number_input("📏 Minimum Height", value=float(row["min_height"]))
                    max_height = st.number_input("📏 Maximum Height", value=float(row["max_height"]))
                    packaging_types = fetch_dropdown("Nursery_Tree_Inventory", "packaging_type")
                    packaging_choice = st.selectbox("📦 Packaging Type", (["Add New"] + packaging_types) if packaging_types else ["Add New"], index=0)
                    packaging_type = st.text_input("Enter Packaging Type", value=row["packaging_type"]) if packaging_choice == "Add New" else packaging_choice
                    price = st.number_input("💰 Price (IQD)", value=float(row["price"]))
                    date = st.date_input("📅 Date", value=pd.to_datetime(row["date"]))
                
                if st.button("💾 Update Inventory Record"):
                    update_query = """
                    UPDATE Nursery_Tree_Inventory SET nursery_name=%s, tree_common_name=%s, quantity_in_stock=%s, 
                    min_height=%s, max_height=%s, packaging_type=%s, price=%s, date=%s
                    WHERE tree_inventory_id=%s;
                    """
                    execute_query(update_query, (nursery_name, tree_common_name, quantity_in_stock, min_height, max_height, packaging_type, price, date, selected_id))
                    st.success("✅ Inventory record updated!")
            
            with action_tabs[1]:
                if st.button("🗑️ Confirm Delete"):
                    delete_query = "DELETE FROM Nursery_Tree_Inventory WHERE tree_inventory_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("🗑️ Inventory record deleted!")
        else:
            st.info("ℹ️ No inventory data available.")

def main():
    local_css()
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🌳 Nursery Tree Inventory Management System</h1>", unsafe_allow_html=True)
    tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])
    
    with tabs[0]:
        handle_inventory("Single Entry")
    
    with tabs[1]:
        handle_inventory("Bulk Entry")
    
    with tabs[2]:
        handle_inventory("Modify/Delete")

if __name__ == "__main__":
    main()
