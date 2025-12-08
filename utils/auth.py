# utils/auth.py
import hashlib
from utils.db import get_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role, mobile):
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed"

    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, hashed_password, role, mobile_number)
            VALUES (%s, %s, %s, %s)
            """,
            (username, hashed_pw, role, mobile),
        )
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        if hasattr(e, "errno") and e.errno == 1062:
            return False, "Username already exists"
        return False, f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    hashed_pw = hash_password(password)
    cursor.execute(
        """
        SELECT username, role, mobile_number
        FROM users
        WHERE username=%s AND hashed_password=%s
        """,
        (username, hashed_pw),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
