import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

CONNECTION_STRING = "postgresql://neondb_owner:npg_YqBVZNepQ18x@ep-orange-bread-a9efjwmt-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

@st.cache_resource(show_spinner=False)
def get_connection():
    try:
        conn = psycopg2.connect(CONNECTION_STRING, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.OperationalError as op_err:
        st.error("Could not connect to the database. Please check your connection settings.")
        raise op_err
    except Exception as e:
        st.error("An unexpected error occurred while connecting to the database.")
        raise e

def run_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            try:
                results = cur.fetchall()
            except psycopg2.ProgrammingError:
                results = None
        conn.commit()
        return results
    except Exception as e:
        st.error(f"Error executing query: {e}")
        raise e

def execute_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
    except Exception as e:
        st.error(f"Error executing query: {e}")
        raise e

def fetch_dropdown(table, column):
    query = f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL;"
    results = run_query(query)
    return [row[column] for row in results] if results else []
