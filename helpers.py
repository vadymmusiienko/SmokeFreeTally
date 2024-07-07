from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3


"""Connect a database"""
def get_db_connection():
    return sqlite3.connect("user_data.db")


"""Execute a sqlite3 query"""
def execute(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Execute the query
        cur.execute(query, params)

        if query.strip().upper().startswith('SELECT'):
            # For SELECT queries, return fetched results
            return cur.fetchall()
        else:
            # For other queries (INSERT, UPDATE, DELETE), commit the transaction
            conn.commit()
    except sqlite3.Error as e:
        # Handle exceptions, print an error message or log it
        print(f"Error executing SQL query: {e}")
        # Optionally, rollback changes if needed
        conn.rollback()
    finally:
        # Always close cursor and connection
        cur.close()
        conn.close()


"""Decoration function"""
# Decorator function that ensures the user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function