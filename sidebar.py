import streamlit as st

def sidebar_menu():
    # Add a title to the sidebar
    st.sidebar.title("Navigation")
    
    # Create buttons for each page
    data_entry_button = st.sidebar.button("Data Entry")
    search_button = st.sidebar.button("Search")
    
    # Determine which button was clicked and return the corresponding option
    if data_entry_button:
        return "Data Entry"
    elif search_button:
        return "Search"
    
    # Default return value (when no button is clicked)
    return None
