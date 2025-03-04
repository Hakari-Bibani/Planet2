import streamlit as st

def sidebar_menu():
    """
    Create a professional sidebar menu with circular navigation buttons.
    
    Returns:
        str: The currently selected page.
    """
    # Custom styling for the sidebar
    st.sidebar.markdown("""
    <style>
    /* Circular button styling */
    div.stButton > button {
        border-radius: 50%;
        width: 80px;
        height: 80px;
        font-size: 14px;
        margin: 5px;
        background-color: #f0f2f6;
        border: 2px solid #4a4a4a;
        color: #333;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #e1e4eb;
        border-color: #007bff;
        color: #007bff;
        transform: scale(1.05);
    }
    
    div.stButton > button:active {
        background-color: #d1d4db;
    }
    
    /* Sidebar title styling */
    .sidebar-title {
        color: #2c3e50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Set the sidebar title with custom class
    st.sidebar.markdown('<h2 class="sidebar-title">Admin Page</h2>', unsafe_allow_html=True)

    # Initialize session state for page selection if not already set
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Data Entry"

    # Layout buttons side by side using columns
    col1, col2 = st.sidebar.columns(2)

    # Create buttons with consistent styling
    if col1.button("Data Entry", key="data_entry_btn"):
        st.session_state.selected_page = "Data Entry"

    if col2.button("Search", key="search_btn"):
        st.session_state.selected_page = "Search"

    return st.session_state.selected_page
