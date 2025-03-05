import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

def nurseries_page():
    st.title("Nurseries Management")

    # Create tabs for each section
    action_tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])

    # -------------------------
    # SINGLE ENTRY TAB
    # -------------------------
    with action_tabs[0]:
        st.subheader("Add Single Nursery")

        registration_code = st.text_input("Registration Code")
        nursery_name = st.text_input("Nursery Name")
        address = st.text_input("Address")
        contact_name = st.text_input("Contact Name")
        contact_phone = st.text_input("Contact Phone")
        google_map_link = st.text_input("Google Map Link")
        additional_notes = st.text_area("Additional Notes")

        if st.button("Add Nursery"):
            query = """
            INSERT INTO Nurseries 
                (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nursery_name) DO UPDATE 
            SET
                registration_code = EXCLUDED.registration_code,
                address = EXCLUDED.address,
                contact_name = EXCLUDED.contact_name,
                contact_phone = EXCLUDED.contact_phone,
                google_map_link = EXCLUDED.google_map_link,
                additional_notes = EXCLUDED.additional_notes;
            """

            execute_query(
                query,
                (
                    registration_code,
                    nursery_name,
                    address,
                    contact_name,
                    contact_phone,
                    google_map_link,
                    additional_notes
                )
            )
            st.success("Nursery added or updated successfully!")

    # -------------------------
    # BULK ENTRY TAB
    # -------------------------
    with action_tabs[1]:
        st.subheader("Bulk Add Nurseries")

        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            df = pd.read_csv(file)
            # Ensure columns are lowercase to match DB fields properly
            df.columns = df.columns.str.lower()  

            for index, row in df.iterrows():
                query = """
                INSERT INTO Nurseries 
                    (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nursery_name) DO UPDATE 
                SET
                    registration_code = EXCLUDED.registration_code,
                    address = EXCLUDED.address,
                    contact_name = EXCLUDED.contact_name,
                    contact_phone = EXCLUDED.contact_phone,
                    google_map_link = EXCLUDED.google_map_link,
                    additional_notes = EXCLUDED.additional_notes;
                """

                execute_query(
                    query,
                    (
                        row.get("registration_code", ""),
                        row["nursery_name"],
                        row["address"],
                        row["contact_name"],
                        row["contact_phone"],
                        row["google_map_link"],
                        row.get("additional_notes", "")
                    )
                )
            st.success("Bulk nurseries added or updated!")

    # -------------------------
    # MODIFY/DELETE TAB
    # -------------------------
    with action_tabs[2]:
        st.subheader("Modify/Delete Nurseries")

        # Retrieve current Nurseries
        query = "SELECT * FROM Nurseries;"
        data = run_query(query)

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

# Nursery ID is assumed to be the unique key
            selected_id = st.selectbox("Select Nursery ID to Modify/Delete", df["nursery_id"])
            action_choice = st.radio("Action", ["Modify", "Delete"])

            if action_choice == "Delete":
                if st.button("Delete Nursery"):
                    delete_query = "DELETE FROM Nurseries WHERE nursery_id = %s;"
                    execute_query(delete_query, (selected_id,))
                    st.success("Nursery deleted!")
            else:
                # Modify
                row = df[df["nursery_id"] == selected_id].iloc[0]

                registration_code = st.text_input("Registration Code", value=row["registration_code"])
                nursery_name = st.text_input("Nursery Name", value=row["nursery_name"])
                address = st.text_input("Address", value=row["address"])
                contact_name = st.text_input("Contact Name", value=row["contact_name"])
                contact_phone = st.text_input("Contact Phone", value=row["contact_phone"])
                google_map_link = st.text_input("Google Map Link", value=row["google_map_link"])
                additional_notes = st.text_area("Additional Notes", value=row["additional_notes"])

                if st.button("Update Nursery"):
                    update_query = """
                    UPDATE Nurseries 
                    SET 
                        registration_code=%s,
                        nursery_name=%s,
                        address=%s,
                        contact_name=%s,
                        contact_phone=%s,
                        google_map_link=%s,
                        additional_notes=%s
                    WHERE nursery_id=%s;
                    """
                    execute_query(
                        update_query, 
                        (
                            registration_code,
                            nursery_name,
                            address,
                            contact_name,
                            contact_phone,
                            google_map_link,
                            additional_notes,
                            selected_id
                        )
                    )
                    st.success("Nursery updated!")
