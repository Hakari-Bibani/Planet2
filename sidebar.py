import streamlit as st

def sidebar_menu():
    """
    Create a professional, modern sidebar menu with vertical navigation.
    
    Returns:
        str: The currently selected page.
    """
    # Custom sidebar styling
    st.sidebar.markdown("""
    <style>
    /* Sidebar container styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }

    /* Professional sidebar title */
    .sidebar-title {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        padding: 15px 0;
        border-bottom: 2px solid #007bff;
        margin-bottom: 20px;
        font-size: 1.5em;
    }

    /* Navigation buttons */
    .stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        border: 2px solid #007bff;
        color: #007bff;
        font-weight: 600;
        text-transform: uppercase;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #007bff;
        color: white;
        transform: scale(1.02);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .stButton > button:focus {
        outline: none;
        border-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar title with professional styling
    st.sidebar.markdown('<div class="sidebar-title">Admin Dashboard</div>', unsafe_allow_html=True)

    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Data Entry"

    # Create navigation buttons
    if st.sidebar.button("📋 Data Entry", use_container_width=True):
        st.session_state.selected_page = "Data Entry"

    if st.sidebar.button("🔍 Search", use_container_width=True):
        st.session_state.selected_page = "Search"

    return st.session_state.selected_page
