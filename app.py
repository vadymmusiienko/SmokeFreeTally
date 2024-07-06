# External libraries/frameworks
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from cs50 import SQL

# My libraries
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# TODO Configure CS50 library to use SQLite database

# Handle cash
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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
        # TODO check user's login and password, redirect to "/" if matches
        return "Error"
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")