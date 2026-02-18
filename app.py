import sqlite3
from flask import Flask, session, redirect, render_template, \
                  request, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import config
import dog

app = Flask(__name__, template_folder=".")
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    dogs = dog.get_dogs()
    return render_template("html/index.html", dogs=dogs, session=session)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    print("here")
    sql = "SELECT * FROM dogs WHERE id = ?"
    dog= db.query(sql, [dog_id])
    if not dog:
        abort(404)
    return render_template("html/dog.html", dog=dog[0])

@app.route("/create_dog")
def create_dog_form():
    dog_breeds = dog.get_breeds()
    return render_template("html/create_dog.html", dog_breeds=dog_breeds)

@app.route("/create_dog", methods=["POST"])
def create_dog():
    registration_number = request.form["registration_number"]
    name = request.form["name"]
    breed = request.form["breed"]
    born_date = request.form["born_date"]
    sex = request.form["sex"]

    if not registration_number or not name or not breed or not born_date or not sex:
        return "ERROR: all fields are required"

    try:
        sql = "INSERT INTO Dogs (registration_number, name, breed, born_date, sex) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, [registration_number, name, breed, born_date, sex])
    except sqlite3.IntegrityError as e:
        print(e)
        return "ERROR: registration failed"
    return redirect("/")

@app.route("/register")
def register():
    return render_template("html/register.html")

@app.route("/login")
def login_form():
    return render_template("html/login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return "ERROR: invalid username or password"

    password_hash = result[0][0]
    if not check_password_hash(password_hash, password):
        return "ERROR: invalid username or password"

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
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
