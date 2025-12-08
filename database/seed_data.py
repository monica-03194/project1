# seed_data.py (final fix)
import pandas as pd
import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1212",
    "database": "client_query_db",
    "port": 3308
}

CSV_PATH = "queries.csv"

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def seed_queries():
    df = pd.read_csv(CSV_PATH)

    # Convert dates safely
    df["date_raised"] = pd.to_datetime(df["date_raised"], errors="coerce")
    df["date_closed"] = pd.to_datetime(df["date_closed"], errors="coerce")

    # 🔥 FIX STATUS VALUES
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()

    # Only allow Open or Closed — everything else becomes Open
    df["status"] = df["status"].apply(lambda x: "Open" if x not in ["Open", "Closed"] else x)

    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO queries
        (query_id, client_email, client_mobile, query_heading,
         query_description, status, date_raised, date_closed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_sql, (
            row["query_id"],
            row["client_email"],
            str(row["client_mobile"]),
            row["query_heading"],
            row["query_description"],
            row["status"],
            row["date_raised"],
            row["date_closed"],
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ CSV data inserted successfully!")

if __name__ == "__main__":
    seed_queries()
