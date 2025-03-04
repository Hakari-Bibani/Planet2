import streamlit as st
import pandas as pd
import handle

def nurseries_page(pool):
    st.header("Manage Nurseries")
    # Add nursery form
    with st.form("nursery_form", clear_on_submit=True):
        name = st.text_input("Nursery Name *")
        address = st.text_area("Address")
        submitted = st.form_submit_button("Add Nursery")
    if submitted and name:
        handle.add_nursery(pool, name=name, address=address)
        st.success(f"Nursery '{name}' added.")
    # Bulk upload nurseries
    st.subheader("Bulk Upload Nurseries")
    file = st.file_uploader("Upload CSV of nurseries", type=["csv"])
    if file:
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            handle.add_nursery(pool, **row.to_dict())
        st.success(f"Uploaded {len(df)} nurseries.")
    # Edit/delete existing
    st.subheader("Existing Nurseries")
    nurseries = handle.get_all_nurseries(pool)
    names = [""] + [n["name"] for n in nurseries]
    choice = st.selectbox("Select Nursery to Edit/Delete", names)
    if choice:
        nursery = next(n for n in nurseries if n["name"] == choice)
        new_name = st.text_input("Nursery Name", value=nursery["name"])
        new_address = st.text_area("Address", value=nursery.get("address",""))
        if st.button("Update Nursery"):
            handle.update_nursery(pool, nursery_id=nursery["id"], name=new_name, address=new_address)
            st.success("Nursery updated.")
        if st.button("Delete Nursery"):
            handle.delete_nursery(pool, nursery_id=nursery["id"])
            st.warning("Nursery deleted.")

