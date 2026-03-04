import sqlite3
from flask import Flask, make_response, session, redirect, render_template, \
                  request, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import config
import dog
import user

app = Flask(__name__, template_folder=".")
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    result = dog.get_dogs()
    if not result:
        abort(404)
    return render_template("html/index.html", dogs=result, session=session)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    result = dog.get_dog(dog_id)
    if not result:
        abort(404)
    return render_template("html/dog.html", dog=result)

@app.route("/create_dog")
def create_dog_form():
    require_login()
    dog_breeds = dog.get_breeds()
    championship_titles = dog.get_championship_titles()
    return render_template("html/create_dog.html", dog_breeds=dog_breeds, championship_titles=championship_titles)

@app.route("/my_dogs")
def show_my_dogs():
    require_login()
    owner_id = session["user_id"]
    my_dogs = dog.get_owners_dogs(owner_id)
    return render_template("html/my_dogs.html", my_dogs=my_dogs)

@app.route("/create_dog", methods=["POST"])
def create_dog():
    require_login()
    registration_number = request.form["registration_number"]
    name = request.form["name"]
    color = request.form["color"]
    breed = request.form["breed"]
    birth_date = request.form["birth_date"]
    sex = request.form["sex"]
    owner_id = session["user_id"]

    if not registration_number or not name or not breed or not birth_date or not sex or not owner_id:
        return "ERROR: all fields are required"

    try:
        sql = "INSERT INTO Dogs (registration_number, name, color, breed, birth_date, sex, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        db.execute(sql, [registration_number, name, color, breed, birth_date, sex, owner_id])
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
    
    user_id = user.get_id_with_username(username)

    session["username"] = username
    session["user_id"] = user_id
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
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
@app.route("/image/<int:dog_id>")
def show_image(dog_id):
    image = dog.get_image(dog_id)
    if not image:
        abort(404)

    if isinstance(image, (bytes, bytearray, memoryview)):
        data = bytes(image)
        response = make_response(data)
        response.headers.set("Content-Type", "image/jpeg")
        return response

    if isinstance(image, str):
        pictures_dir = os.path.join(app.root_path, "static", "pictures")
        return send_from_directory(pictures_dir, image)

    try:
        data = str(image).encode("utf-8")
        response = make_response(data)
        response.headers.set("Content-Type", "image/jpeg")
        return response
    except Exception:
        abort(404)

def require_login():
    if "user_id" not in session:
        abort(403)