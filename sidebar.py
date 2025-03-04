import streamlit as st

def show_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Data Entry", "Search"])
    return page
