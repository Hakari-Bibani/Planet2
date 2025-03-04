import psycopg2
import streamlit as st

@st.experimental_singleton
def get_connection():
    conn = psycopg2.connect("postgresql://neondb_owner:npg_YqBVZNepQ18x@ep-orange-bread-a9efjwmt-pooler.gwc.azure.neon.tech/neondb?sslmode=require")
    return conn

def run_query(query, params=None, fetch=True):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    if fetch:
        result = cur.fetchall()
    else:
        result = None
    conn.commit()
    cur.close()
    return result
