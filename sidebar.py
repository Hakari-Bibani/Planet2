import streamlit as st
import streamlit_shadcn_ui as ui

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

    /* Circular navigation buttons */
    .nav-button {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 15px auto;
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

    .nav-button:hover {
        background-color: #007bff;
        color: white;
        transform: scale(1.05);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    .nav-button:focus {
        outline: none;
        border-color: #0056b3;
    }

    /* Active button state */
    .nav-button.active {
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar title with professional styling
    st.sidebar.markdown('<div class="sidebar-title">Admin Dashboard</div>', unsafe_allow_html=True)

    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Data Entry"

    # Create vertical navigation buttons
    def create_nav_button(label):
        """
        Create a styled navigation button.
        
        Args:
            label (str): Text for the navigation button
        
        Returns:
            bool: Whether the button was clicked
        """
        button_class = "nav-button active" if st.session_state.selected_page == label else "nav-button"
        return st.sidebar.button(label, key=f"{label.lower().replace(' ', '_')}_btn", 
                                 use_container_width=True,
                                 help=f"Navigate to {label} page")

    # Navigation buttons
    if create_nav_button("Data Entry"):
        st.session_state.selected_page = "Data Entry"

    if create_nav_button("Search"):
        st.session_state.selected_page = "Search"

    # Optional: Add a separator or additional nav items
    st.sidebar.divider()

    # Optional additional navigation or utility buttons
    if st.sidebar.button("📊 Analytics", key="analytics_btn", use_container_width=True):
        st.session_state.selected_page = "Analytics"

    if st.sidebar.button("⚙️ Settings", key="settings_btn", use_container_width=True):
        st.session_state.selected_page = "Settings"

    return st.session_state.selected_page
