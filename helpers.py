from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3




# Function to create tables in a sqlite3 database
def create_table(conn, table):
    # Create a table
    create_table = """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    

# Create a SQLite database
conn = sqlite3.connect('user_data.db')
conn.close()

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