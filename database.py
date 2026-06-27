import sqlite3

DATABASE = "users.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            username TEXT PRIMARY KEY,

            violations INTEGER DEFAULT 0,

            blocked_until TEXT DEFAULT NULL

        )
    """)

    conn.commit()

    conn.close()

def create_user(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR IGNORE INTO users(username)

        VALUES(?)

    """, (username,))

    conn.commit()

    conn.close()

def get_user(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM users

        WHERE username=?

    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user

def update_violations(username, violations):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET violations=?

        WHERE username=?

    """, (violations, username))

    conn.commit()

    conn.close()

def update_block(username, blocked_until):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET blocked_until=?

        WHERE username=?

    """, (blocked_until, username))

    conn.commit()

    conn.close()