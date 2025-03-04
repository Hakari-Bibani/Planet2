import streamlit as st
from pages import data_entry, search

st.set_page_config(page_title="Planet2", layout="wide")
menu = st.sidebar.radio("Navigation", ["Data Entry", "Search"])
if menu == "Data Entry":
    data_entry.app()
elif menu == "Search":
    search.app()
