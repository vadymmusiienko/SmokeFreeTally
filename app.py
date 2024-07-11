# External libraries/frameworks
from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# My libraries
from helpers import login_required, info_required, execute

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

        "user_info": """
            CREATE TABLE IF NOT EXISTS user_info (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                cigarettes_per_day INTEGER NOT NULL,
                pack_cost INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
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
@info_required
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
        return render_template("login&layout.html")
    
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
        return redirect("/info")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# Enter your info page
@app.route("/info", methods=["GET", "POST"])
@login_required
def info():
    user_id = session["user_id"]

    if request.method == "POST":
        
        first_name = request.form.get("first_name").strip().lower().capitalize()
        last_name = request.form.get("last_name").strip().lower().capitalize()
        email = request.form.get("email")
        cigarettes_per_day = request.form.get("cigarettes_per_day")
        pack_cost = request.form.get("pack_cost")

        # Ensure all fields were provided
        if not first_name or not last_name or not email or not cigarettes_per_day or not pack_cost:
            return "All fields are required"

        # Ensure pack_cost and cigarettes_per_day are numbers
        try:
            cigarettes_per_day = int(cigarettes_per_day)
            pack_cost = int(pack_cost)
        except ValueError:
            return "Cigarettes and packs must be numbers"

        query = """
            INSERT INTO user_info (user_id, first_name, last_name, email, cigarettes_per_day, pack_cost) VALUES (?, ?, ?, ?, ?, ?) 
            ON CONFLICT(user_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            email = EXCLUDED.email,
            cigarettes_per_day = EXCLUDED.cigarettes_per_day,
            pack_cost = EXCLUDED.pack_cost
        """
        
        execute(query, (user_id, first_name, last_name, email, cigarettes_per_day, pack_cost))

        flash("You have succesfully updated your information!")
        return redirect("/")
        

    else:
        # Check if it's users first time filling out the information page
        query = "SELECT * FROM user_info WHERE user_id = ?"
        user_info = execute(query, (user_id,))
        return render_template("info.html", user_info=user_info[0] if user_info else None)

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