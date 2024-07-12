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

"""Change user's lungs depending on how many total logs they have"""
def check_lungs(total_logs):
    # Different lungs skins
    lungs_1 = "lungs_1.png"
    lungs_2 = "lungs_2.png"
    lungs_3 = "lungs_3.png"
    lungs_4 = "lungs_4.png"
    lungs_5 = "lungs_5.png"

    # Determine which skin to use and return a path to it
    if total_logs < 5:
        return lungs_1
    
    elif total_logs < 10:
        return lungs_2
    
    elif total_logs < 15:
        return lungs_3
    
    elif total_logs < 30:
        return lungs_4

    else: 
        return  lungs_5



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