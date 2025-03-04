import streamlit as st
import nurseries
import trees
import inventory

def set_page_style():
    """Set custom page style to make the application look more professional."""
    st.set_page_config(
        page_title="Nursery Management System",
        page_icon="🌱",
        layout="wide"
    )
    
    # Custom CSS for a more modern and clean look
    st.markdown("""
    <style>
    /* Base styling */
    body {
        font-family: 'Inter', 'Roboto', sans-serif;
        background-color: #f4f6f9;
    }
    
    /* Header styling */
    .main-title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 10px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
        border-radius: 8px;
        padding: 10px 20px;
        margin: 0 5px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f2f6;
    }
    
    /* Form input styling */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #d1d8e0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 6px;
        border: 1px solid #d1d8e0;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def data_entry_page():
    set_page_style()
    
    st.markdown("<h1 class='main-title'>🌿 Nursery Management System</h1>", unsafe_allow_html=True)
    
    # Create tabs for different tables
    tab_names = ["Nurseries", "Trees", "Nursery Tree Inventory"]
    tabs = st.tabs(tab_names)
    
    # Handling each tab
    with tabs[0]:  # Nurseries Tab
        st.markdown("### Nursery Management")
        entry_type = st.radio("Entry Type", 
                               ["Single Entry", "Bulk Entry", "Modify/Delete"], 
                               horizontal=True)
        nurseries.handle_nurseries(entry_type)
    
    with tabs[1]:  # Trees Tab
        st.markdown("### Tree Management")
        entry_type = st.radio("Entry Type", 
                               ["Single Entry", "Bulk Entry", "Modify/Delete"], 
                               horizontal=True)
        trees.handle_trees(entry_type)
    
    with tabs[2]:  # Inventory Tab
        st.markdown("### Nursery Tree Inventory")
        entry_type = st.radio("Entry Type", 
                               ["Single Entry", "Bulk Entry", "Modify/Delete"], 
                               horizontal=True)
        inventory.handle_inventory(entry_type)

def main():
    data_entry_page()

if __name__ == "__main__":
    main()
