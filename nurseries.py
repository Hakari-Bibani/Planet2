import streamlit as st
import pandas as pd
import re
from handle import run_query, execute_query, fetch_dropdown

def validate_input(field, value):
    """Validate input fields with basic rules."""
    if field == "registration_code":
        # Ensure registration code is alphanumeric and not empty
        return bool(re.match(r'^[A-Za-z0-9-]+$', value)) if value else False
    
    elif field == "nursery_name":
        # Ensure nursery name is not empty and has at least 2 characters
        return len(value.strip()) >= 2
    
    elif field == "contact_phone":
        # Basic phone number validation
        return bool(re.match(r'^\+?1?\d{10,14}$', value.replace(' ', '')) if value else False)
    
    elif field == "google_map_link":
        # Optional field, but validate URL if provided
        return not value or bool(re.match(r'^https?://\S+$', value))
    
    return True

def display_error_message(field):
    """Display specific error messages for different fields."""
    error_messages = {
        "registration_code": "Invalid registration code. Use alphanumeric characters.",
        "nursery_name": "Nursery name must be at least 2 characters long.",
        "contact_phone": "Invalid phone number format.",
        "google_map_link": "Invalid Google Maps link format."
    }
    st.error(error_messages.get(field, "Invalid input"))

def handle_nurseries(entry_type):
    # Use container for better visual organization
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stContainer {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        if entry_type == "Single Entry":
            st.markdown("## 🌱 Add Single Nursery")
            st.markdown("---")
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                registration_code = st.text_input("Registration Code *", help="Unique identifier for the nursery")
                nursery_name = st.text_input("Nursery Name *", help="Full name of the nursery")
                contact_name = st.text_input("Contact Name", help="Name of primary contact person")
            
            with col2:
                address = st.text_input("Address", help="Full physical address")
                contact_phone = st.text_input("Contact Phone", help="Contact phone number")
                google_map_link = st.text_input("Google Map Link", help="Optional link to nursery location")
            
            additional_notes = st.text_area("Additional Notes", help="Any extra information about the nursery")
            
            # Validation before submission
            if st.button("Add Nursery", type="primary"):
                # Check all validations
                validation_errors = []
                
                if not validate_input("registration_code", registration_code):
                    validation_errors.append("registration_code")
                
                if not validate_input("nursery_name", nursery_name):
                    validation_errors.append("nursery_name")
                
                if contact_phone and not validate_input("contact_phone", contact_phone):
                    validation_errors.append("contact_phone")
                
                if google_map_link and not validate_input("google_map_link", google_map_link):
                    validation_errors.append("google_map_link")
                
                if validation_errors:
                    for error in validation_errors:
                        display_error_message(error)
                else:
                    query = """
                    INSERT INTO Nurseries (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (nursery_name) DO UPDATE SET
                        registration_code = EXCLUDED.registration_code,
                        address = EXCLUDED.address,
                        contact_name = EXCLUDED.contact_name,
                        contact_phone = EXCLUDED.contact_phone,
                        google_map_link = EXCLUDED.google_map_link,
                        additional_notes = EXCLUDED.additional_notes;
                    """
                    execute_query(query, (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes))
                    st.success("✅ Nursery added or updated successfully!")
                    st.balloons()

        elif entry_type == "Bulk Entry":
            st.markdown("## 📦 Bulk Add Nurseries")
            st.markdown("---")
            
            st.info("""
            📌 Bulk upload instructions:
            - Ensure CSV file has columns: registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes
            - Column names are case-insensitive
            - Missing optional columns will be filled with empty values
            """)
            
            file = st.file_uploader("Upload CSV", type=["csv"], help="Select a CSV file for bulk nursery entry")
            
            if file is not None:
                try:
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.lower()
                    
                    st.markdown("### Preview of Uploaded Data")
                    st.dataframe(df)
                    
                    if st.button("Confirm Bulk Upload", type="primary"):
                        progress_bar = st.progress(0)
                        
                        for index, row in df.iterrows():
                            progress_bar.progress((index + 1) / len(df))
                            
                            query = """
                            INSERT INTO Nurseries (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (nursery_name) DO UPDATE SET
                                registration_code = EXCLUDED.registration_code,
                                address = EXCLUDED.address,
                                contact_name = EXCLUDED.contact_name,
                                contact_phone = EXCLUDED.contact_phone,
                                google_map_link = EXCLUDED.google_map_link,
                                additional_notes = EXCLUDED.additional_notes;
                            """
                            execute_query(query, (
                                row.get("registration_code", ""),
                                row["nursery_name"],
                                row.get("address", ""),
                                row.get("contact_name", ""),
                                row.get("contact_phone", ""),
                                row.get("google_map_link", ""),
                                row.get("additional_notes", "")
                            ))
                        
                        st.success("🎉 Bulk nurseries added or updated!")
                        st.balloons()
                
                except Exception as e:
                    st.error(f"Error processing file: {e}")

        elif entry_type == "Modify/Delete":
            st.markdown("## 🔧 Modify/Delete Nurseries")
            st.markdown("---")
            
            query = "SELECT * FROM Nurseries;"
            data = run_query(query)
            
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_id = st.selectbox("Select Nursery ID", df["nursery_id"])
                
                with col2:
                    action = st.radio("Action", ["Modify", "Delete"], horizontal=True)
                
                if action == "Delete":
                    if st.button("Confirm Delete", type="primary"):
                        delete_query = "DELETE FROM Nurseries WHERE nursery_id = %s;"
                        execute_query(delete_query, (selected_id,))
                        st.warning(f"Nursery with ID {selected_id} deleted!")
                
                else:
                    row = df[df["nursery_id"] == selected_id].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        registration_code = st.text_input("Registration Code", value=row["registration_code"])
                        nursery_name = st.text_input("Nursery Name", value=row["nursery_name"])
                        contact_name = st.text_input("Contact Name", value=row["contact_name"])
                    
                    with col2:
                        address = st.text_input("Address", value=row["address"])
                        contact_phone = st.text_input("Contact Phone", value=row["contact_phone"])
                        google_map_link = st.text_input("Google Map Link", value=row["google_map_link"])
                    
                    additional_notes = st.text_area("Additional Notes", value=row["additional_notes"])
                    
                    if st.button("Update Nursery", type="primary"):
                        update_query = """
                        UPDATE Nurseries SET registration_code=%s, nursery_name=%s, address=%s, contact_name=%s, contact_phone=%s, google_map_link=%s, additional_notes=%s
                        WHERE nursery_id=%s;
                        """
                        execute_query(update_query, (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes, selected_id))
                        st.success("Nursery updated successfully! 🌟")
