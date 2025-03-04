import streamlit as st
from handle import run_query, fetch_dataframe

def add_nursery(data):
    query = """
    INSERT INTO "Nurseries" 
    ("Registration_code", "Nursery_name", "Address", "Contact_name", "Contact_phone", "Google_map_link", "Additional_notes")
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data.get("Registration_code"), data.get("Nursery_name"), data.get("Address"),
        data.get("Contact_name"), data.get("Contact_phone"), data.get("Google_map_link"),
        data.get("Additional_notes")
    )
    run_query(query, params)

def get_all_nurseries():
    query = 'SELECT * FROM "Nurseries"'
    return fetch_dataframe(query)

def nursery_data_entry():
    st.subheader("Nursery Data Entry (Single)")
    with st.form("nursery_entry_form"):
        registration_code = st.text_input("Registration Code")
        nursery_name = st.text_input("Nursery Name")
        address = st.text_input("Address")
        contact_name = st.text_input("Contact Name")
        contact_phone = st.text_input("Contact Phone")
        google_map_link = st.text_input("Google Map Link")
        additional_notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Add Nursery")
        if submitted:
            data = {
                "Registration_code": registration_code,
                "Nursery_name": nursery_name,
                "Address": address,
                "Contact_name": contact_name,
                "Contact_phone": contact_phone,
                "Google_map_link": google_map_link,
                "Additional_notes": additional_notes,
            }
            add_nursery(data)
            st.success("Nursery added successfully!")
