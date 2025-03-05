import streamlit as st
import pandas as pd
from handle import run_query, execute_query, fetch_dropdown

# Custom CSS for improved styling
def local_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e6e9ef;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #3498db;
            color: white;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 6px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def handle_nurseries(entry_type):
    """
    Handles logic for each entry type: "Single Entry", "Bulk Entry", and "Modify/Delete".
    """
    # Styling for form headers
    st.markdown(
        f"<h2 style='color: #2c3e50; text-align: center;'>{entry_type} Form</h2>", 
        unsafe_allow_html=True
    )

    # -----------------------
    # SINGLE ENTRY SECTION
    # -----------------------
    if entry_type == "Single Entry":
        # Create two columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            registration_code = st.text_input("🏷️ Registration Code", help="Unique identifier for the nursery")
            nursery_name = st.text_input("🌱 Nursery Name", help="Official name of the nursery")
            address = st.text_input("📍 Address", help="Full physical address")

        with col2:
            contact_name = st.text_input("👤 Contact Name", help="Primary contact person")
            contact_phone = st.text_input("📞 Contact Phone", help="Contact telephone number")
            google_map_link = st.text_input("🗺️ Google Map Link", help="Link to nursery location on Google Maps")

        additional_notes = st.text_area("📝 Additional Notes", help="Any extra information about the nursery")

        if st.button("Add Nursery", key="single_entry_submit"):
            query = """
                INSERT INTO Nurseries 
                    (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
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
                registration_code, 
                nursery_name, 
                address, 
                contact_name, 
                contact_phone, 
                google_map_link, 
                additional_notes
            ))
            st.success("✅ Nursery added or updated successfully!")

    # -----------------------
    # BULK ENTRY SECTION
    # -----------------------
    elif entry_type == "Bulk Entry":
        st.markdown(
            """
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3>📄 Bulk Nursery Upload</h3>
            <p>Upload a CSV file with nursery details. Ensure columns match:</p>
            <p><b>registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        file = st.file_uploader("Upload CSV", type=["csv"], help="CSV file with nursery details")
        if file is not None:
            df = pd.read_csv(file)
            # Ensure headers are lowercase to match DB fields
            df.columns = df.columns.str.lower()  

            # Preview uploaded data
            st.write("Preview of Uploaded Data:")
            st.dataframe(df)

            if st.button("Confirm Bulk Upload"):
                for _, row in df.iterrows():
                    query = """
                        INSERT INTO Nurseries 
                            (registration_code, nursery_name, address, contact_name, contact_phone, google_map_link, additional_notes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (nursery_name) DO UPDATE SET
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
                            row["registration_code"],
                            row["nursery_name"],
                            row["address"],
                            row["contact_name"],
                            row["contact_phone"],
                            row["google_map_link"],
                            row.get("additional_notes", "")
                        )
                    )
                st.success("✅ Bulk nurseries added or updated!")

    # -----------------------
    # MODIFY/DELETE SECTION
    # -----------------------
    elif entry_type == "Modify/Delete":
        query = "SELECT * FROM Nurseries;"
        data = run_query(query)

        if data:
            df = pd.DataFrame(data)

            st.markdown(
                """
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <h3>🌿 Nursery Management</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Show current data
            st.dataframe(df, use_container_width=True)

            # Create two columns: left for selection, right for tabs
            col1, col2 = st.columns([1, 2])

            with col1:
                selected_id = st.selectbox("Select Nursery ID", df["nursery_id"])

            with col2:
                # Create tabs for Modify and Delete
                modify_tab, delete_tab = st.tabs(["Modify", "Delete"])

                with modify_tab:
                    row = df[df["nursery_id"] == selected_id].iloc[0]

                    # Split fields into two columns again for editing
                    c1, c2 = st.columns(2)
                    with c1:
                        registration_code = st.text_input("Registration Code", value=row["registration_code"])
                        nursery_name = st.text_input("Nursery Name", value=row["nursery_name"])
                        address = st.text_input("Address", value=row["address"])

                    with c2:
                        contact_name = st.text_input("Contact Name", value=row["contact_name"])
                        contact_phone = st.text_input("Contact Phone", value=row["contact_phone"])
                        google_map_link = st.text_input("Google Map Link", value=row["google_map_link"])

                    additional_notes = st.text_area("Additional Notes", value=row["additional_notes"])

                    if st.button("Update Nursery", key="update_nursery"):
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
                        st.success("✅ Nursery updated successfully!")

                with delete_tab:
                    st.write("Are you sure you want to delete this nursery?")
                    if st.button("Confirm Delete", key="delete_nursery"):
                        delete_query = "DELETE FROM Nurseries WHERE nursery_id = %s;"
                        execute_query(delete_query, (selected_id,))
                        st.success("🗑️ Nursery deleted successfully!")
        else:
            st.info("No nursery data available.")

def main():
    # Apply custom CSS
    local_css()

    # Main app title
    st.markdown(
        "<h1 style='text-align: center; color: #2c3e50;'>🌱 Nursery Management System</h1>",
        unsafe_allow_html=True
    )

    # Main-level tabs for the three entry types
    tabs = st.tabs(["Single Entry", "Bulk Entry", "Modify/Delete"])

    with tabs[0]:
        handle_nurseries("Single Entry")
    with tabs[1]:
        handle_nurseries("Bulk Entry")
    with tabs[2]:
        handle_nurseries("Modify/Delete")

if __name__ == "__main__":
    main()


