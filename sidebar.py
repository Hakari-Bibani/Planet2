import streamlit as st

def sidebar_menu():
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose Page", ("Data Entry", "Search"))
    return option
