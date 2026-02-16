import sqlite3
from flask import Flask
from flask import redirect, render_template, request, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db

app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("html/index.html")

@app.route("/register")
def register():
    return render_template("html/register.html")

@app.route("/login")
def login():
    return render_template("html/login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return "ERROR: invalid username or password"

    password_hash = result[0][0]
    if not check_password_hash(password_hash, password):
        return "ERROR: invalid username or password"

    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    email = request.form["email"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not email or not password1 or not password2:
        return "ERROR: all fields are required"
    if password1 != password2:
        return "ERROR: passwords do not match"
    elif len(password1) < 8:
        return "ERROR: password must be atleast 8 characters long"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
        db.execute(sql, [username, email, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username or email already exists"

    return redirect("/")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
