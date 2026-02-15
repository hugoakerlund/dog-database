import sqlite3
from flask import Flask
from flask import redirect, render_template, request, send_from_directory
from werkzeug.security import generate_password_hash
import os
import db

app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("html/index.html")

@app.route("/register")
def register():
    return render_template("html/register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords do not match"
    elif len(password1) < 8:
        return "ERROR: password must be atleast 8 characters long"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username already exists"

    return "Account created successfully"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
