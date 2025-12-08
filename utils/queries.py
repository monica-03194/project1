# utils/queries.py
from datetime import datetime
import pandas as pd
from utils.db import get_connection

def generate_query_id():
    """
    Generates IDs like Q0001, Q0002, ...
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT query_id FROM queries ORDER BY query_id DESC LIMIT 1")
    row = cursor.fetchone()

    if not row:
        new_id = "Q0001"
    else:
        last_id = row[0]  # e.g. "Q0012"
        num = int(last_id[1:]) + 1
        new_id = f"Q{num:04d}"

    cursor.close()
    conn.close()
    return new_id

def insert_query(client_email, client_mobile, query_heading, query_description):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    query_id = generate_query_id()
    date_raised = datetime.now()

    cursor.execute(
        """
        INSERT INTO queries
        (query_id, client_email, client_mobile, query_heading,
         query_description, status, date_raised, date_closed)
        VALUES (%s, %s, %s, %s, %s, 'Open', %s, NULL)
        """,
        (query_id, client_email, client_mobile, query_heading, query_description, date_raised),
    )

    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_queries(status_filter=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    query = "SELECT * FROM queries"
    params = []

    if status_filter and status_filter != "All":
        query += " WHERE status=%s"
        params.append(status_filter)

    query += " ORDER BY date_raised DESC"

    df = pd.read_sql(query, conn, params=params if params else None)
    conn.close()
    return df

def close_query(query_id):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE queries
        SET status='Closed', date_closed=%s
        WHERE query_id=%s AND status='Open'
        """,
        (datetime.now(), query_id),
    )
    conn.commit()
    success = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return success
