# utils/db.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import streamlit as st

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None
    