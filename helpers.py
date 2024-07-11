from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3


"""Execute a SQL query with the given parameters and return the result."""
def execute(sql_query, params=()):
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute(sql_query, params)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


"""Ensures the user provided the required information"""
def settings_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        query = "SELECT * FROM user_info WHERE user_id = ?"
        user_info = execute(query, (user_id,))
        if not user_info:
            return redirect("/settings")
        return f(*args, **kwargs)
    
    return decorated_function

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