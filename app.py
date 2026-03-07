import sqlite3
from flask import Flask, make_response, session, redirect, render_template, \
                  request, send_from_directory, abort, flash
import os
import config
import dog
import user
import input
import litter

app = Flask(__name__, template_folder=".")
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    result = dog.get_dogs()
    if not result:
        abort(404, "ERROR: no dogs found")
    return render_template("html/index.html", dogs=result, session=session)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    result = dog.get_dog(dog_id)
    if not result:
        abort(404, "ERROR: dog not found")
    return render_template("html/dog.html", dog=result)

@app.route("/my_dogs")
def show_my_dogs():
    require_login()
    owner_id = session["user_id"]
    my_dogs = user.get_users_dogs(owner_id)
    return render_template("html/my_dogs.html", my_dogs=my_dogs)

@app.route("/create_dog", methods=["GET", "POST"])
def create_dog():
    require_login()
    if request.method == "POST":
        form = input.get_dog_creation_form_data(request)
        try:
            dog.insert_dog(form)
        except sqlite3.IntegrityError as e:
            print(f"Database error: {e}")
            return "ERROR: registration failed (duplicate registration number or invalid references)"
        return redirect("/")

    elif request.method == "GET":
        colors = dog.get_colors()
        dog_breeds = dog.get_breeds()
        championship_titles = dog.get_championship_titles()
        return render_template("html/create_dog.html", colors=colors, dog_breeds=dog_breeds,
                               championship_titles=championship_titles)

@app.route("/update_dog/<int:dog_id>", methods=["POST"])
def update_dog(dog_id):
    require_login()
    form = input.get_dog_creation_form_data(request)
    try:
        dog.update_dog(dog_id, form)
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        return "ERROR: update failed (duplicate registration number or invalid references)"
    return redirect("/my_dogs")

@app.route("/remove/<int:dog_id>", methods=["GET", "POST"])
def remove(dog_id):
    require_login()
    if request.method == "GET":
        dog_info = dog.get_dog(dog_id)
        if not dog_info:
            abort(404, "ERROR: dog not found")
        return render_template("html/remove.html", dog=dog_info)

    elif request.method == "POST":
        dog.delete_dog(dog_id)
        return redirect("/my_dogs")

@app.route("/edit/<int:dog_id>")
def edit_form(dog_id):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")
    dog_breeds = dog.get_breeds()
    championship_titles = dog.get_championship_titles()
    return render_template("html/edit.html", dog=dog_info, dog_breeds=dog_breeds,
                           championship_titles=championship_titles)

@app.route("/register")
def register():
    return render_template("html/register.html")

@app.route("/login")
def login_form():
    return render_template("html/login.html")

@app.route("/login", methods=["POST"])
def login():
    user_id, username = user.check_login(request)
    set_session(user_id, username)
    return redirect("/")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    form = input.get_account_registration_form_data(request)
    try:
        user.insert_user(form)
        flash("Account created successfully!", "success")
    except sqlite3.IntegrityError:
        return "ERROR: username or email already exists"
    set_session(user.get_id_with_username(form["username"]), form["username"])
    return redirect("/")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/image/<int:dog_id>")
def show_image(dog_id):
    image = dog.get_image(dog_id)
    if not image:
        abort(404, "ERROR: image not found")

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
        abort(404, "ERROR: unable to display image")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user_info = user.get_user(user_id)
    users_dogs = user.get_users_dogs(user_id)
    if not user_info:
        abort(404, "ERROR: user not found")
    return render_template("html/user.html", user=user_info, dogs=users_dogs)

@app.route("/litter/<int:litter_id>")
def show_litter(litter_id):
    litter_info = litter.get_litter(litter_id)
    dogs = litter.get_dogs_in_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")
    return render_template("html/litter.html", litter=litter_info, dogs=dogs)

def require_login():
    if "user_id" not in session:
        abort(403, "ERROR: login required")

def set_session(user_id, username):
    session["user_id"] = user_id
    session["username"] = username