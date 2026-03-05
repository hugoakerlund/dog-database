import sqlite3
from flask import Flask, make_response, session, redirect, render_template, \
                  request, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
import os
import db
import config
import dog
import user
import input

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
    
    registration_number = request.form.get("registration_number", "").strip()
    name = request.form.get("name", "").strip()
    image = request.files.get("image")
    color = request.form.get("color", "").strip()
    breed = request.form.get("breed", "").strip()
    birth_date = request.form.get("birth_date", "").strip()
    death_date = request.form.get("death_date", "").strip() or None # Field is optional
    sex = request.form.get("sex", "").strip()
    father_id = request.form.get("father_id", "").strip() or None # Field is optional
    mother_id = request.form.get("mother_id", "").strip() or None # Field is optional
    championship_title = request.form.get("championship_title", "").strip() or None
    owner_id = session["user_id"]

    print("Received form data:")
    print(f"Registration: {registration_number}, Name: {name}, Image: {image.filename if image else 'None'}")

    if not registration_number or not name or not breed or not birth_date or not sex:
        return "ERROR: registration number, name, breed, birth date, and sex are required"
    
    if not input.validate_registration_number(registration_number):
        return "ERROR: invalid registration number format (must be 'FI12345/67')"

    if not input.validate_name(name):
        return "ERROR: name must be between 2 and 20 characters"
    
    if not input.validate_date(birth_date):
        return "ERROR: invalid birth date format (must be YYYY-MM-DD)"

    if death_date and not input.validate_date(death_date):
        return "ERROR: invalid death date format (must be YYYY-MM-DD)"
    
    if father_id and not input.validate_registration_number(father_id):
        return "ERROR: invalid father registration number format (must be 'FI12345/67')"

    if mother_id and not input.validate_registration_number(mother_id):
        return "ERROR: invalid mother registration number format (must be 'FI12345/67')"

    if not image or not image.filename:
        return "ERROR: image is required"
    
    if not image.filename.lower().endswith(('.jpg', '.jpeg')):
        return "ERROR: only .jpg and .jpeg images are allowed"

    image_data = image.read()
    
    if len(image_data) > 100 * 1024:
        return "ERROR: image size must be less than 100KB"

    championship_title_id = None
    if championship_title:
        championship_title_id = dog.get_championship_title_id(championship_title)

    father_dog_id = None
    mother_dog_id = None
    
    if father_id:
        father_dog_id = dog.get_dog_id_by_registration_number(father_id)
        if not father_dog_id:
            return f"ERROR: father with registration number '{father_id}' not found"
    
    if mother_id:
        mother_dog_id = dog.get_dog_id_by_registration_number(mother_id)
        if not mother_dog_id:
            return f"ERROR: mother with registration number '{mother_id}' not found"

    try:
        sql = """INSERT INTO Dogs (registration_number, name, image, color, breed, 
                                   birth_date, death_date, sex, father_id, mother_id, 
                                   owner_id, championship_title_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        db.execute(sql, [registration_number, name, image_data, color, breed, birth_date, 
                         death_date, sex, father_dog_id, mother_dog_id, owner_id, championship_title_id])
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        return "ERROR: registration failed (duplicate registration number or invalid references)"
    return redirect("/")

@app.route("/remove/<int:dog_id>", methods=["GET", "POST"])
def remove(dog_id):
    require_login()
    if request.method == "GET":
        dog_info = dog.get_dog(dog_id)
        if not dog_info:
            abort(404)
        return render_template("html/remove.html", dog=dog_info)

    elif request.method == "POST":
        dog.delete_dog(dog_id)
        return redirect("/my_dogs")

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