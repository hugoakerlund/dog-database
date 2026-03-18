import sqlite3
from flask import Flask, make_response, session, redirect, render_template, \
                  request, send_from_directory, abort, flash
import math
import os
import config
import dog
import dog_show
import owner
import input
import litter
import secrets

app = Flask(__name__, template_folder=".")
app.secret_key = config.SECRET_KEY

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    dog_count = dog.get_dog_count()
    page_count = math.ceil(dog_count / page_size)
    page_count = max(page_count, 1)
    dogs = dog.get_dogs(page, page_size)
    if not dogs:
        abort(404, "ERROR: no dogs found")
    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/", str(page_count))

    return render_template("html/index.html", page=page, page_count=page_count,
                            dogs=dogs, session=session)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = dog.search(query) if query else []
    return render_template("html/search.html", query=query, results=results)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    result = dog.get_dog(dog_id)
    if not result:
        abort(404, "ERROR: dog not found")
    return render_template("html/dog.html", dog=result, session=session)

@app.route("/my_dogs")
def show_my_dogs():
    require_login()
    owner_id = session["owner_id"]
    my_dogs = owner.get_dogs(owner_id)
    return render_template("html/my_dogs.html", my_dogs=my_dogs)

@app.route("/my_litters")
def show_my_litters():
    require_login()
    owner_id = session["owner_id"]
    my_litters = owner.get_litters(owner_id)
    return render_template("html/my_litters.html", my_litters=my_litters)

@app.route("/create_dog", methods=["GET"])
def create_dog_get():
    colors = dog.get_colors()
    dog_breeds = dog.get_breeds()
    championship_titles = dog.get_championship_titles()
    return render_template("html/create_dog.html", colors=colors, dog_breeds=dog_breeds,
                        championship_titles=championship_titles)

@app.route("/create_dog", methods=["POST"])
def create_dog_post():
    require_login()
    check_csrf()
    form = input.get_dog_form(request)
    if not input.check_dog_form(form, edit=False):
        return redirect("/create_dog")
    try:
        dog.insert_dog(form)
    except sqlite3.IntegrityError as e:
        return f"ERROR: Database error: {e} (possibly duplicate name or invalid foreign key)"
    return redirect("/")

@app.route("/create_litter", methods=["GET"])
def create_litter_get():
    require_login()
    return render_template("html/create_litter.html")

@app.route("/create_litter", methods=[ "POST"])
def create_litter_post():
    require_login()
    check_csrf()
    form = input.get_litter_form(request)
    if not input.check_litter_form(form):
        return render_template("html/create_litter.html")
    try:
        litter.insert_litter(form)
    except sqlite3.IntegrityError as e:
        return f"ERROR: Database error: {e} (possibly invalid foreign key)"
    return redirect("/litters")

@app.route("/edit_dog/<int:dog_id>", methods=["GET"])
def edit_dog_get(dog_id):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")
    colors = dog.get_colors()
    dog_breeds = dog.get_breeds()
    championship_titles = dog.get_championship_titles()
    return render_template("html/edit_dog.html", dog=dog_info, colors=colors, dog_breeds=dog_breeds,
                        championship_titles=championship_titles)

@app.route("/edit_dog/<int:dog_id>", methods=["POST"])
def edit_dog_post(dog_id):
    require_login()
    form = input.get_dog_form(request)
    old_registration_number = dog.get_registration_number(dog_id)
    if not input.check_dog_form(form, edit=True, old_registration_number=old_registration_number):
        return redirect(f"/edit_dog/{dog_id}")
    try:
        dog.update_dog(dog_id, form)
    except sqlite3.IntegrityError as e:
        return f"ERROR: Database error: {e} (possibly invalid foreign key)"
    return redirect("/my_dogs")

@app.route("/remove_dog/<int:dog_id>", methods=["GET"])
def remove_dog_get(dog_id):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info or dog_info["owner_id"] != session["owner_id"]:
        abort(404, "ERROR: dog not found")
    return render_template("html/remove_dog.html", dog=dog_info)

@app.route("/remove_dog/<int:dog_id>", methods=["POST"])
def remove_dog_post(dog_id):
    require_login()
    check_csrf()
    if "continue" in request.form:
        dog.delete_dog(dog_id)
    return redirect("/my_dogs")

@app.route("/edit_litter/<int:litter_id>", methods=["GET"])
def edit_litter_get(litter_id):
    require_login()
    litter_info = litter.get_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")
    return render_template("html/edit_litter.html", litter=litter_info)

@app.route("/edit_litter/<int:litter_id>", methods=["POST"])
def edit_litter_post(litter_id):
    require_login()
    form = input.get_litter_form(request)
    old_litter_name = litter.get_litter(litter_id)["name"]
    if not input.check_litter_form(form, edit=True, old_litter_name=old_litter_name):
        return redirect(f"/edit_litter/{litter_id}")
    try:
        litter.update_litter(litter_id, form)
    except sqlite3.IntegrityError as e:
        return f"ERROR: Database error: {e} (possibly invalid foreign key)"
    return redirect("/my_litters")

@app.route("/remove_litter/<int:litter_id>", methods=["GET"])
def remove_litter_get(litter_id):
    require_login()
    litter_info = litter.get_litter(litter_id)
    if not litter_info or litter_info["owner_id"] != session["owner_id"]:
        abort(404, "ERROR: litter not found")
    return render_template("html/remove_litter.html", litter=litter_info)

@app.route("/remove_litter/<int:litter_id>", methods=["POST"])
def remove_litter_post(litter_id):
    require_login()
    check_csrf()
    if "continue" in request.form:
        litter.delete_litter(litter_id)
    return redirect("/my_litters")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not input.check_login(request):
            return redirect("/login")
        owner_id = owner.get_id_with_name(request.form.get("name", "").strip())
        name = request.form.get("name", "").strip()
        set_session(owner_id, name)
        return redirect("/")
    elif request.method == "GET":
        return render_template("html/login.html")

@app.route("/logout")
def logout():
    require_login()
    del session["owner_id"]
    del session["name"]
    return redirect("/")

@app.route("/register", methods=["GET"])
def register_get():
    return render_template("html/register.html")

@app.route("/register", methods=["POST"])
def register_post():
    form = input.get_registration_form(request)
    if not input.check_registration_form(form):
        return redirect("/register")
    try:
        owner.insert_owner(form)
        flash("Account created successfully!", "success")
    except sqlite3.IntegrityError as e:
        return f"ERROR: database error {e} (possibly duplicate name or email)"
    set_session(owner.get_id_with_name(form["name"]), form["name"])
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

@app.route("/owner/<int:owner_id>")
def show_owner(owner_id):
    owner_info = owner.get_owner(owner_id)
    owners_dogs = owner.get_dogs(owner_id)
    if not owner_info:
        abort(404, "ERROR: owner not found")
    return render_template("html/owner.html", owner=owner_info, dogs=owners_dogs)

@app.route("/litter/<int:litter_id>")
def show_litter(litter_id):
    litter_info = litter.get_litter(litter_id)
    dogs = litter.get_dogs_in_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")
    return render_template("html/litter.html", litter=litter_info, dogs=dogs)

@app.route("/litters")
@app.route("/litters/<int:page>")
def show_litters(page=1):
    page_size = 10
    litter_count = litter.get_litter_count()
    page_count = math.ceil(litter_count / page_size)
    page_count = max(page_count, 1)
    litters = litter.get_litters(page, page_size)

    if not litters:
        abort(404, "ERROR: no litters found")
    if page < 1:
        return redirect("/litters/1")
    if page > page_count:
        return redirect("/litters/", str(page_count))

    return render_template("html/litters.html", page=page, page_count=page_count, 
                           litters=litters)

@app.route("/owners")
@app.route("/owners/<int:page>")
def show_owners(page=1):
    page_size = 10
    owner_count = owner.get_owner_count()
    page_count = math.ceil(owner_count / page_size)
    page_count = max(page_count, 1)
    owners = owner.get_owners(page, page_size)

    if not owners:
        abort(404, "ERROR: no owners found")
    if page < 1:
        return redirect("/owners/1")
    if page > page_count:
        return redirect("/owners/", str(page_count))

    return render_template("html/owners.html", page=page, page_count=page_count, 
                           owners=owners)

@app.route("/dog_show/<int:show_id>")
def show_dog_show(show_id):
    show_info = dog_show.get_dog_show(show_id)
    dogs = dog_show.get_show_participants(show_id)
    if not show_info:
        abort(404, "ERROR: dog show not found")

    eligible_dogs = []
    if "owner_id" in session:
        owner_dogs = owner.get_dogs(session["owner_id"])
        participant_ids = {d["id"] for d in dogs}
        eligible_dogs = [d for d in owner_dogs if d["id"] not in participant_ids]

    return render_template("html/dog_show.html", show=show_info, dogs=dogs, eligible_dogs=eligible_dogs)


@app.route("/dog_show/<int:show_id>/add", methods=["POST"])
def add_dog_to_show(show_id):
    require_login()
    check_csrf()

    show_info = dog_show.get_dog_show(show_id)
    if not show_info:
        abort(404, "ERROR: dog show not found")

    dog_id = request.form.get("dog_id")
    if not dog_id:
        abort(400, "ERROR: dog not selected")

    try:
        dog_id = int(dog_id)
    except ValueError:
        abort(400, "ERROR: invalid dog id")
    
    if dog.is_dead(dog_id):
        flash("Cannot add dead dog to the show", "error")
        return redirect(f"/dog_show/{show_id}")

    owner_id = session["owner_id"]
    owner_dog_ids = {d["id"] for d in owner.get_dogs(owner_id)}
    if dog_id not in owner_dog_ids:
        abort(403, "ERROR: dog does not belong to you")

    if dog_show.is_participant(show_id, dog_id):
        flash("Dog is already registered for this show", "error")
        return redirect(f"/dog_show/{show_id}")

    try:
        dog_show.add_participant(show_id, dog_id)
        flash("Dog added to show", "success")
    except sqlite3.IntegrityError as e:
        flash(f"ERROR: Database error: {e}", "error")

    return redirect(f"/dog_show/{show_id}")


@app.route("/dog_shows")
@app.route("/dog_shows/<int:page>")
def show_dog_shows(page=1):
    page_size = 10
    dog_show_count = dog_show.get_dog_show_count()
    page_count = math.ceil(dog_show_count / page_size)
    page_count = max(page_count, 1)
    dog_shows = dog_show.get_dog_shows(page, page_size)

    if not dog_shows:
        abort(404, "ERROR: no dog shows found")
    if page < 1:
        return redirect("/dog_shows/1")
    if page > page_count:
        return redirect("/dog_shows/", str(page_count))

    return render_template("html/dog_shows.html", page=page, page_count=page_count, 
                           dog_shows=dog_shows)

def require_login():
    if "owner_id" not in session:
        abort(403, "ERROR: login required")

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403, "ERROR: invalid CSRF token")

def set_session(owner_id, name):
    session["owner_id"] = owner_id
    session["name"] = name
    session["csrf_token"] = secrets.token_hex(16)