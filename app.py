import streamlit as st
from sidebar import show_sidebar
from trees import trees_page
from Nurseries import nurseries_page
from Nursery_Tree_Inventory import inventory_page
from research import search_page
from handle import init_db_pool

# Initialize database connection pool (runs once at app start)
pool = init_db_pool()  # This will create or get the asyncpg pool for NeonDB

# Apply custom CSS for styling (background, text, etc.)
st.markdown("""
<style>
/* Example custom styles */
.stApp { background-color: #f9f9f9; }  /* page background */
footer {visibility: hidden;}          /* hide Streamlit footer */
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
page = show_sidebar()  # returns "Data Entry" or "Search"

if page == "Data Entry":
    # Let user pick which table to manage under Data Entry
    table_choice = st.sidebar.selectbox("Choose Table", ["Trees", "Nurseries", "Inventory"])
    if table_choice == "Trees":
        trees_page(pool)
    elif table_choice == "Nurseries":
        nurseries_page(pool)
    else:
        inventory_page(pool)
elif page == "Search":
    search_page(pool)
