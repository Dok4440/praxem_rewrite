import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        conn = sqlite3.connect("database/praxem.db")
    except Error as e:
        print("'create_connection()' Error occurred: {}".format(e))
        return

    return conn


def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except Error as e:
        print("'execute_query()' Error occurred: {}".format(e))

    return cursor


def select_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        return cursor.execute(f"SELECT {query}").fetchall()

    except Error as e:
        return f"ERROR: {e}"
