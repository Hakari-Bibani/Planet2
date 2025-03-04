import psycopg2
import pandas as pd
import streamlit as st

DB_URL = "postgresql://neondb_owner:npg_YqBVZNepQ18x@ep-orange-bread-a9efjwmt-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

def get_connection():
    return psycopg2.connect(DB_URL)

def run_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if query.strip().lower().startswith("select"):
                result = cur.fetchall()
            else:
                conn.commit()
                result = None
    except Exception as e:
        conn.rollback()
        st.error(f"Database error: {e}")
        result = None
    finally:
        conn.close()
    return result

def fetch_dataframe(query, params=None):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df
