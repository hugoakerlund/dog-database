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
    dogs = dog.get_dogs()
    return render_template("html/index.html", dogs=dogs, session=session)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    sql = "SELECT * FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    if not result:
        abort(404)
    owner_id = dog.get_owner_id(dog_id)
    username = user.get_username_with_id(owner_id)
    father_id = result[0][10]
    mother_id = result[0][11]
    father_registration_number = dog.get_registration_number(father_id) if father_id else None
    mother_registration_number = dog.get_registration_number(mother_id) if mother_id else None
    championship_title_id = result[0][14]
    championship_title = dog.get_championship_title(championship_title_id)
    return render_template("html/dog.html", dog=result[0], username=username[0][0], 
                           championship_title=championship_title, father_registration_number=father_registration_number, 
                           mother_registration_number=mother_registration_number)

@app.route("/create_dog")
def create_dog_form():
    dog_breeds = dog.get_breeds()
    return render_template("html/create_dog.html", dog_breeds=dog_breeds)

@app.route("/my_dogs")
def show_my_dogs():
    owner_id = session["user_id"]
    my_dogs = dog.get_owners_dogs(owner_id)
    return render_template("html/my_dogs.html", my_dogs=my_dogs)

@app.route("/create_dog", methods=["POST"])
def create_dog():
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