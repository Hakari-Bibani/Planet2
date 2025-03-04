import streamlit as st
from sidebar import sidebar_menu

selected_page = sidebar_menu()

if selected_page == "Data Entry":
    import table
    table.data_entry_page()
elif selected_page == "Search":
    import search
    search.search_page()
