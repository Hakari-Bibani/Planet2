import streamlit as st

def sidebar_menu():
    st.sidebar.title("Admin Page")

    # Inject custom CSS to style the buttons as circles
    st.sidebar.markdown("""
    <style>
    div.stButton > button {
        border-radius: 50%;
        width: 80px;
        height: 80px;
        font-size: 14px;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for page selection if not already set
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Data Entry"

    # Layout buttons side by side using columns
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Data Entry"):
        st.session_state.selected_page = "Data Entry"
    if col2.button("Search"):
        st.session_state.selected_page = "Search"

    return st.session_state.selected_page
