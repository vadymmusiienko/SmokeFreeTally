# External libraries/frameworks
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# My libraries
from helpers import login_required, execute

"""Configure flask"""
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Handle cash
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


"""Set up a data base"""
def setup_database():
    """Set up the SQLite database and create tables if they don't exist."""
    # Dictionary of tables for the database
    TABLES = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """,
        # Other tables go here
    }

    # Connect to SQLite database (create if not exists)
    conn = sqlite3.connect('user_data.db')

    # Create a cursor for the database to execute commands
    cur = conn.cursor()

    # Create tables in the database if they don't exist
    for _, create_table_sql in TABLES.items():
        cur.execute(create_table_sql) 

    # Commit changes to save the table creation
    conn.commit()

    # Close the database connection
    conn.close()

# Set up the database when the script is executed
setup_database()


"""Configure routs"""
# Home page
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was provided
        username = request.form.get("username")
        if not username:
            # TODO error html
            return "must provide username"
        
        # Ensure password was provided
        password = request.form.get("password")
        if not password:
            # TODO error html
            return "must provide password"

        # Query database for username
        sql_query = "SELECT password FROM users WHERE username = ?"
        hashed_password = execute(sql_query, (username,))

        # Ensure username exists and password is correct
        if len(hashed_password) != 1 or not check_password_hash(hashed_password[0][0], password):
            # TODO error html
            return "invalid username and/or password"
        
        # Remember which user has logged in
        sql_query = "SELECT id FROM users WHERE username = ?"
        user_id = execute(sql_query, (username,))
        user_id = user_id[0][0]
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("password-confirm")

        # Ensure username was submitted
        if not username:
            # TODO error html
            return "must provide username"

        # Ensure password was submitted
        if not password:
            # TODO error html
            return "must provide password"

        # Ensure confirmation was submitted
        if not confirmation:
            # TODO error html
            return "must confirm your password"

        # Ensure password matches the confirmation
        if password != confirmation:
            # TODO error html
            return "the password does not match"
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Add user to the data base
        try:
            sql_query = "INSERT INTO users (username, password) VALUES (?, ?)"
            execute(sql_query, (username, hashed_password))
        except sqlite3.IntegrityError:
            return "the user already exists"
        

        # Remember which user has logged in
        sql_query = "SELECT id FROM users WHERE username = ?"
        user_id = execute(sql_query, (username,))
        user_id = user_id[0][0]
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    
# Reset password page
@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("password-confirm")

        # Ensure username was submitted
        if not username:
            # TODO error html
            return "must provide username"

        # Ensure password was submitted
        if not password:
            # TODO error html
            return "must provide password"

        # Ensure confirmation was submitted
        if not confirmation:
            # TODO error html
            return "must confirm your password"

        # Ensure password matches the confirmation
        if password != confirmation:
            # TODO error html
            return "the password does not match"
        
        # Ensure the user has an account
        sql_query = "SELECT id FROM users WHERE username = ?"
        user_id = execute(sql_query, (username,))
        if not user_id:
            # TODO error html
            return "incorrect username"

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Change user's password
        sql_query = "UPDATE users SET password = ? WHERE username = ?"
        execute(sql_query, (hashed_password, username))
        
        # Remember which user has logged in
        user_id = user_id[0][0]
        session["user_id"] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("resetpassword.html")


if __name__ == '__main__':
    app.run(debug=True)