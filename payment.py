import streamlit as st
import pandas as pd
from handle import run_query, execute_query

def handle_payments(entry_type):
    """
    Payment management interface.
    Only Modify/Delete functionality is available for payments.
    """
    st.markdown("<h2 style='color: #2c3e50; text-align: center;'>Payment Modify/Delete</h2>", unsafe_allow_html=True)
    
    query = "SELECT * FROM payments;"
    data = run_query(query)
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        selected_id = st.selectbox("Select Payment ID to Modify/Delete", df["payment_id"])
        action_tabs = st.tabs(["Modify", "Delete"])
        
        with action_tabs[0]:
            row = df[df["payment_id"] == selected_id].iloc[0]
            
            tree_name = st.text_input("Tree Name", value=row["tree_name"])
            customer_full_name = st.text_input("Customer Full Name", value=row["customer_full_name"])
            username = st.text_input("Username", value=row["username"])
            quantity = st.text_input("Quantity", value=row["quantity"])
            amount = st.text_input("Amount", value=row["amount"])
            address = st.text_input("Address", value=row["address"])
            whatsapp_number = st.text_input("Whatsapp Number", value=row["whatsapp_number"])
            email = st.text_input("Email", value=row["email"])
            payment_preference = st.text_input("Payment Preference", value=row["payment_preference"])
            payment_date = st.text_input("Payment Date", value=row["payment_date"])
            status = st.text_input("Status", value=row["status"])
            note = st.text_area("Note", value=row["note"])
            
            if st.button("Update Payment"):
                update_query = """
                UPDATE payments 
                SET tree_name=%s, customer_full_name=%s, username=%s, quantity=%s, amount=%s, address=%s,
                    whatsapp_number=%s, email=%s, payment_preference=%s, payment_date=%s, status=%s, note=%s
                WHERE payment_id=%s;
                """
                execute_query(update_query, (
                    tree_name, customer_full_name, username, quantity, amount, address,
                    whatsapp_number, email, payment_preference, payment_date, status, note, selected_id
                ))
                st.success("Payment updated successfully!")
                
        with action_tabs[1]:
            if st.button("Confirm Delete"):
                delete_query = "DELETE FROM payments WHERE payment_id = %s;"
                execute_query(delete_query, (selected_id,))
                st.success("Payment deleted successfully!")
    else:
        st.info("No payment data available.")
