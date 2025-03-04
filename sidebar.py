import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Data Entry", "Search"])
    return page
