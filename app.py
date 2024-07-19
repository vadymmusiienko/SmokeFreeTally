# External libraries/frameworks
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import sqlite3

# My libraries
from helpers import login_required, settings_required, execute, check_lungs

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
                gender TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """,

        "log_history": """
            CREATE TABLE IF NOT EXISTS log_history (
                user_id INTEGER PRIMARY KEY,
                first_log TEXT,
                last_log TEXT,
                total_logs INTEGER NOT NULL DEFAULT 0,
                streak INTEGER NOT NULL DEFAULT 0,
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
@app.route("/", methods=["GET", "POST"])
@login_required
@settings_required
def index():
    # Get user's id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":    

        # Get the log data from the db
        query = "SELECT * FROM log_history WHERE user_id = ?"
        log_history = execute(query, (user_id,))

        # Get current date and time
        current_datetime = datetime.now()

        # Ensure it's been a day since the last log-in, redirect if NOT (if the first login ever - skip)
        if log_history[0][1] is not None:
            datetime_format = "%Y-%m-%d %H:%M:%S.%f"
            if current_datetime < (datetime.strptime(log_history[0][2], datetime_format) + timedelta(hours=24)):
                return redirect("/")

        # First smoke free day
        if log_history[0][1] is None:
            
            # Insert the first log history into the table
            query = "UPDATE log_history SET first_log = ?, last_log = ?, total_logs = 1, streak = 1"
            execute(query, (current_datetime, current_datetime))
        
        # Not the first log-in
        else:
            # Get the data
            last_log, total_logs, streak = log_history[0][2:]

            # Convert datatime string to an actual object
            datetime_format = "%Y-%m-%d %H:%M:%S.%f"
            last_log = datetime.strptime(last_log, datetime_format)

            # Update the total logs
            total_logs += 1

            # If the last log date was yesterday, increment the streak
            if last_log.date() == current_datetime.date() - timedelta(days=1):
                streak += 1

            # If the last log date was not yesterday or today, reset the streak
            elif last_log.date() != current_datetime.date():
                streak = 1

            # Update the log history
            query = "UPDATE log_history SET last_log = ?, total_logs = ?, streak = ? WHERE user_id = ?"
            execute(query, (current_datetime, total_logs, streak, user_id))
        
        # Redirect back to the home back via GET
        return redirect("/")
            

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get personal user's information
        query = "SELECT * FROM user_info WHERE user_id = ?"
        first_name, last_name, email, cigarettes_per_day, pack_cost, gender = execute(query, (user_id,))[0][1:]
        # todo gender that I don't use yet
        # Get the log history
        query = "SELECT last_log, total_logs, streak FROM log_history WHERE user_id = ?"
        last_log, total_logs, streak = execute(query, (user_id,))[0]

        # Do the math to calculate "cigarettes not smoked" and "Money Saved"
        cigarettes_not_smoked = cigarettes_per_day * total_logs
        money_saved = round((pack_cost * (cigarettes_not_smoked / 20)), 2)

        # Disable the button depending on whether it's time to login
        current_datetime = datetime.now()
        if last_log is not None:
            datetime_format = "%Y-%m-%d %H:%M:%S.%f"
            disabled = current_datetime < (datetime.strptime(last_log, datetime_format) + timedelta(hours=24))
        else:
            disabled = False

        # Change user's lungs with progress
        lungs = check_lungs(total_logs)

        # Create a dictionary with the informatoin
        information = {
            "cigarettes_not_smoked": cigarettes_not_smoked,
            "money_saved": money_saved,
            "total_logs": total_logs,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "streak": streak,
            "disabled": disabled,
            "last_log": last_log,
            "gender": gender,
            "lungs": lungs,
        }

        return render_template("index.html", information=information)

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
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
            execute(query, (username, hashed_password))
        except sqlite3.IntegrityError:
            return "the user already exists"
        

        # Remember which user has logged in
        query = "SELECT id FROM users WHERE username = ?"
        user_id = execute(query, (username,))
        user_id = user_id[0][0]
        session["user_id"] = user_id


        # Create a log history for a user (with 2 NULL values)
        query = "INSERT INTO log_history (user_id, first_log, last_log, total_logs, streak) VALUES (?, NULL, NULL, 0, 0)"
        execute(query, (user_id,))

        # Redirect user to home page
        return redirect("/settings")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# Enter your info page
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # Get user's id
    user_id = session["user_id"]

    if request.method == "POST":
        
        first_name = request.form.get("first_name").strip().lower().capitalize()
        last_name = request.form.get("last_name").strip().lower().capitalize()
        email = request.form.get("email")
        cigarettes_per_day = request.form.get("cigarettes_per_day")
        pack_cost = request.form.get("pack_cost")
        gender = request.form.get("gender").strip().lower()

        # Ensure all fields were provided
        if not first_name or not last_name or not email or not cigarettes_per_day or not pack_cost or not gender:
            return "All fields are required"

        # Ensure pack_cost and cigarettes_per_day are numbers
        try:
            cigarettes_per_day = int(cigarettes_per_day)
            pack_cost = int(pack_cost)
        except ValueError:
            return "Cigarettes and packs must be numbers"

        query = """
            INSERT INTO user_info (user_id, first_name, last_name, email, cigarettes_per_day, pack_cost, gender) VALUES (?, ?, ?, ?, ?, ?, ?) 
            ON CONFLICT(user_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            email = EXCLUDED.email,
            cigarettes_per_day = EXCLUDED.cigarettes_per_day,
            pack_cost = EXCLUDED.pack_cost,
            gender = EXCLUDED.gender
        """
        
        execute(query, (user_id, first_name, last_name, email, cigarettes_per_day, pack_cost, gender))

        return redirect("/")
        

    else:
        # Check if it's users first time filling out the information page
        query = "SELECT * FROM user_info WHERE user_id = ?"
        user_info = execute(query, (user_id,))

        # Change user's lungs with progress
        query = "SELECT total_logs FROM log_history WHERE user_id = ?"
        total_logs = execute(query, (user_id,))[0][0]
        lungs = check_lungs(total_logs)

        # Make a dictionary with all the information
        if user_info:
            user_info = user_info[0]
            user_information = {
                "first_name": user_info[1],
                "last_name": user_info[2],
                "email": user_info[3],
                "cigarettes_per_day": user_info[4],
                "pack_cost": user_info[5],
                "gender": user_info[6],
            }
        else:
            user_information = None

        return render_template("settings.html", user_information=user_information if user_information is not None else None, lungs=lungs)

# About page
@app.route("/about")
@settings_required
def about():
    return render_template("about.html")

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