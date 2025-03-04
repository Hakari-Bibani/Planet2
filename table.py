import streamlit as st
import nurseries
import trees
import inventory

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

def data_entry_page():
    local_css()
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Data Entry</h1>", unsafe_allow_html=True)

    table_option = st.selectbox("Select Table", ["Nurseries", "Trees", "Nursery_Tree_Inventory"])
    tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])
    
    with tabs[0]:
        entry_type = "Single Entry"
        if table_option == "Nurseries":
            nurseries.handle_nurseries(entry_type)
        elif table_option == "Trees":
            trees.handle_trees(entry_type)
        elif table_option == "Nursery_Tree_Inventory":
            inventory.handle_inventory(entry_type)
    
    with tabs[1]:
        entry_type = "Bulk Entry"
        if table_option == "Nurseries":
            nurseries.handle_nurseries(entry_type)
        elif table_option == "Trees":
            trees.handle_trees(entry_type)
        elif table_option == "Nursery_Tree_Inventory":
            inventory.handle_inventory(entry_type)
    
    with tabs[2]:
        entry_type = "Modify/Delete"
        if table_option == "Nurseries":
            nurseries.handle_nurseries(entry_type)
        elif table_option == "Trees":
            trees.handle_trees(entry_type)
        elif table_option == "Nursery_Tree_Inventory":
            inventory.handle_inventory(entry_type)
