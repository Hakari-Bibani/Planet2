import streamlit as st

def show_sidebar():
    st.sidebar.title("Nursery Inventory App")
    page = st.sidebar.radio("Go to page:", ["Data Entry", "Search"])
    return page

