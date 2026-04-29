import math
import os
import secrets
from urllib.parse import urlencode
import markupsafe
from flask import Flask, make_response, session, redirect, render_template, \
    request, send_from_directory, abort, flash
import config
import dog
import dog_show
import owner
import input_validator
import litter

app = Flask(__name__, template_folder=".")
app.secret_key = config.SECRET_KEY

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    dog_count = dog.get_dog_count()
    page_count = math.ceil(dog_count / page_size)
    page_count = max(page_count, 1)
    dogs = dog.get_dogs(page, page_size)

    if page < 1:
        return redirect("/1")

    if page > page_count:
        return redirect("/" + str(page_count))

    return render_template("html/index.html", page=page, page_count=page_count,
                           dogs=dogs, session=session)

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    query = request.args.get("query")

    page_size = 10
    result_count = dog.get_search_count(query)
    page_count = math.ceil(result_count / page_size)
    page_count = max(page_count, 1)
    results = dog.search(query, page, page_size) if query else []

    if page < 1:
        qs = urlencode({"query": query})
        return redirect(f"/search/1/?{qs}")

    if page > page_count:
        qs = urlencode({"query": query})
        return redirect(f"/search/{page_count}/?{qs}")

    return render_template("html/search.html", page=page, page_count=page_count,
                           result_count=result_count, query=query, results=results)

@app.route("/dog/<int:dog_id>")
def show_dog(dog_id):
    dog_info  = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")

    participated_shows = dog_show.get_dog_participated_shows(dog_id)
    comments = dog.get_comments(dog_id)
    return render_template("html/dog.html", dog=dog_info, comments=comments,
                           participated_shows=participated_shows, session=session)

@app.route("/dog/new", methods=["GET"])
def create_dog_get(filled=None):
    require_login()
    colors = dog.get_colors()
    dog_breeds = dog.get_breeds()
    owner_id = session["owner_id"]
    my_litters = owner.get_litters(owner_id)
    return render_template("html/create_dog.html", filled=filled, colors=colors,
                           dog_breeds=dog_breeds, litters=my_litters)

@app.route("/dog/new", methods=["POST"])
def create_dog_post():
    require_login()
    check_csrf()
    form = input_validator.get_dog_form(request)
    if not input_validator.check_dog_form(form):
        return create_dog_get(form)

    dog.insert_dog(form)
    flash("Dog created successfully!", "success")
    return redirect(f"/owner/{session['owner_id']}")

@app.route("/comment/new", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()
    form = input_validator.get_comment_form(request)
    if not input_validator.check_comment_form(form):
        return redirect(f"/dog/{form['dog_id']}")

    dog.insert_comment(form)
    flash("Comment added successfully!", "success")
    return redirect(f"/dog/{form['dog_id']}")

@app.route("/comment/<int:comment_id>/remove", methods=["POST"])
def remove_comment(comment_id):
    require_login()
    require_owner(owner.get_comment_owner_id(comment_id))
    check_csrf()
    dog_id = request.form.get("dog_id", "") or None
    if not dog_id:
        abort(404, "ERROR: dog not found")

    else:
        dog.remove_comment(comment_id)
        flash("Comment removed successfully!", "success")

    return redirect(f"/dog/{dog_id}")

@app.route("/comment/<int:comment_id>/edit", methods=["GET"])
def edit_comment_get(comment_id, filled=None):
    require_login()
    require_owner(owner.get_comment_owner_id(comment_id))
    comment = dog.get_comment(comment_id)
    if not comment:
        abort(404, "ERROR: comment not found")

    return render_template("html/edit_comment.html", filled=filled, comment=comment)

@app.route("/comment/<int:comment_id>/edit", methods=["POST"])
def edit_comment_post(comment_id):
    require_login()
    require_owner(owner.get_comment_owner_id(comment_id))
    check_csrf()
    form = input_validator.get_comment_form(request, True)
    if "continue" in request.form:
        form = input_validator.get_comment_form(request, True)
        if not input_validator.check_comment_form(form, edit=True):
            return edit_comment_get(comment_id, form)

        dog.update_comment(form)
        flash("Comment updated successfully!", "success")

    return redirect(f"/dog/{form['dog_id']}")

@app.route("/dog/<int:dog_id>/edit", methods=["GET"])
def edit_dog_get(dog_id, filled=None):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")

    require_owner(dog_info["owner_id"])
    colors = dog.get_colors()
    dog_breeds = dog.get_breeds()
    owner_id = session["owner_id"]
    my_litters = owner.get_litters(owner_id)
    participated_shows = dog_show.get_dog_participated_shows(dog_id)
    return render_template("html/edit_dog.html", filled=filled, dog=dog_info,
                           colors=colors,dog_breeds=dog_breeds, litters=my_litters,
                           participated_shows=participated_shows)

@app.route("/dog/<int:dog_id>/edit", methods=["POST"])
def edit_dog_post(dog_id):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")
    require_owner(dog_info["owner_id"])
    check_csrf()
    form = input_validator.get_dog_form(request)
    if not input_validator.check_dog_form(form, edit=True):
        return edit_dog_get(dog_id, form)

    dog.update_dog(dog_id, form)
    flash("Dog updated successfully!", "success")
    return redirect(f"/owner/{session['owner_id']}")

@app.route("/dog/<int:dog_id>/remove", methods=["GET"])
def remove_dog_get(dog_id):
    require_login()
    dog_info = dog.get_dog(dog_id)
    if not dog_info:
        abort(404, "ERROR: dog not found")

    require_owner(session["owner_id"])
    return render_template("html/remove_dog.html", dog=dog_info)

@app.route("/dog/<int:dog_id>/remove", methods=["POST"])
def remove_dog_post(dog_id):
    require_login()
    require_owner(dog.get_owner_id(dog_id))
    check_csrf()
    if "continue" in request.form:
        dog.delete_dog(dog_id)
        flash("Dog deleted successfully!", "success")
        return redirect(f"/owner/{session['owner_id']}")

    return redirect(f"/dog/{dog_id}")

@app.route("/litter/new", methods=["GET"])
def create_litter_get(filled=None):
    require_login()
    owner_id = session["owner_id"]
    male_dogs = owner.get_male_dogs(owner_id)
    female_dogs = owner.get_female_dogs(owner_id)
    return render_template("html/create_litter.html", filled=filled,
                           male_dogs=male_dogs, female_dogs=female_dogs)

@app.route("/litter/new", methods=[ "POST"])
def create_litter_post():
    require_login()
    check_csrf()
    form = input_validator.get_litter_form(request)
    if not input_validator.check_litter_form(form):
        return create_litter_get(form)

    litter.insert_litter(form)
    flash("Litter created successfully!", "success")
    return redirect(f"/owner/{session['owner_id']}")


@app.route("/litter/<int:litter_id>/edit", methods=["GET"])
def edit_litter_get(litter_id, filled=None):
    require_login()
    litter_info = litter.get_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")

    require_owner(litter_info["owner_id"])
    owner_id = session["owner_id"]
    male_dogs = owner.get_male_dogs(owner_id)
    female_dogs = owner.get_female_dogs(owner_id)
    return render_template("html/edit_litter.html", filled=filled, litter=litter_info,
                           male_dogs=male_dogs, female_dogs=female_dogs)

@app.route("/litter/<int:litter_id>/edit", methods=["POST"])
def edit_litter_post(litter_id):
    require_login()
    require_owner(litter.get_litter(litter_id)["owner_id"])
    check_csrf()
    form = input_validator.get_litter_form(request)
    if not input_validator.check_litter_form(form, edit=True):
        return edit_litter_get(litter_id, form)

    litter.update_litter(litter_id, form)
    flash("Litter edited successfully!", "success")
    return redirect(f"/owner/{session['owner_id']}")

@app.route("/litter/<int:litter_id>/remove", methods=["GET"])
def remove_litter_get(litter_id):
    require_login()
    litter_info = litter.get_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")

    require_owner(session["owner_id"])
    return render_template("html/remove_litter.html", litter=litter_info)

@app.route("/litter/<int:litter_id>/remove", methods=["POST"])
def remove_litter_post(litter_id):
    require_login()
    require_owner(litter.get_litter(litter_id)["owner_id"])
    check_csrf()
    if "continue" in request.form:
        litter.delete_litter(litter_id)
        flash("Litter deleted successfully!", "success")

    return redirect(f"/owner/{session['owner_id']}")

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("html/login.html")

@app.route("/login", methods=["POST"])
def login_post():
    if not input_validator.check_login(request):
        return redirect("/login")

    owner_id = owner.get_id_with_name(request.form.get("name", "").strip())
    name = request.form.get("name", "").strip()
    set_session(owner_id, name)
    flash("Login successfull!", "success")
    return redirect("/")

@app.route("/logout")
def logout():
    require_login()
    del session["owner_id"]
    del session["name"]
    flash("Logout successfull!", "success")
    return redirect("/")

@app.route("/register", methods=["GET"])
def register_get(filled=None):
    return render_template("html/register.html", filled=filled)

@app.route("/register", methods=["POST"])
def register_post():
    form = input_validator.get_account_form(request)
    if not input_validator.check_account_form(form):
        return register_get(form)

    owner.insert_owner(form)
    set_session(owner.get_id_with_name(form["name"]), form["name"])
    flash("Account created successfully!", "success")
    return redirect("/")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/image/<int:dog_id>")
def show_image(dog_id):
    image = dog.get_image(dog_id)
    if not image:
        abort(404, "ERROR: image not found")

    if isinstance(image, (bytes)):
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
    except (TypeError, UnicodeEncodeError, ValueError):
        abort(404, "ERROR: unable to display image")

@app.route("/owner/<int:owner_id>")
def show_owner(owner_id):
    owner_info = owner.get_owner(owner_id)
    owners_dogs = owner.get_dogs(owner_id)
    owners_litters= owner.get_litters(owner_id)
    if not owner_info:
        abort(404, "ERROR: owner not found")

    return render_template("html/owner.html", owner=owner_info,
                           dogs=owners_dogs, litters=owners_litters, session=session)

@app.route("/owner/<int:owner_id>/remove", methods=["GET"])
def remove_account_get(owner_id):
    require_login()
    require_owner(owner_id)
    return render_template("html/remove_account.html")

@app.route("/owner/<int:owner_id>/remove", methods=["POST"])
def remove_account_post(owner_id):
    require_login()
    check_csrf()
    require_owner(owner_id)
    owner_id = session["owner_id"]
    if "continue" in request.form:
        owner.remove_owner(owner_id)
        flash("Account deleted successfully!", "success")
        logout()
        return redirect("/")

    return redirect(f"/owner/{owner_id}")

@app.route("/owner/<int:owner_id>/edit", methods=["GET"])
def edit_account_get(owner_id, filled=None):
    require_login()
    require_owner(owner_id)
    owner_id = session["owner_id"]
    owner_info = owner.get_owner(owner_id)
    return render_template("html/edit_account.html", filled=filled,
                           owner=owner_info)

@app.route("/owner/<int:owner_id>/edit", methods=["POST"])
def edit_account_post(owner_id):
    require_login()
    require_owner(owner_id)
    check_csrf()
    form = input_validator.get_account_form(request)
    if not input_validator.check_account_form(form, True):
        return edit_account_get(session["owner_id"], form)

    owner.update_owner(form)
    set_session(owner.get_id_with_name(form["name"]), form["name"])
    flash("Account updated successfully!", "success")
    return redirect(f"/owner/{session['owner_id']}")

@app.route("/litter/<int:litter_id>")
def show_litter(litter_id):
    litter_info = litter.get_litter(litter_id)
    if not litter_info:
        abort(404, "ERROR: litter not found")

    dogs = litter.get_dogs_in_litter(litter_id)
    return render_template("html/litter.html", litter=litter_info, dogs=dogs)

@app.route("/litters")
@app.route("/litters/<int:page>")
def show_litters(page=1):
    page_size = 10
    litter_count = litter.get_litter_count()
    page_count = math.ceil(litter_count / page_size)
    page_count = max(page_count, 1)
    litters = litter.get_litters(page, page_size)

    if page < 1:
        return redirect("/litters/1")

    if page > page_count:
        return redirect("/litters/" + str(page_count))

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

    if page < 1:
        return redirect("/owners/1")

    if page > page_count:
        return redirect("/owners/" + str(page_count))

    return render_template("html/owners.html", page=page, page_count=page_count,
                           owners=owners)

@app.route("/dog_show/<int:show_id>/<int:page>")
@app.route("/dog_show/<int:show_id>")
def show_dog_show(show_id, page=1):
    show_info = dog_show.get_dog_show(show_id)
    if not show_info:
        abort(404, "ERROR: dog show not found")


    page_size = 10
    dog_count = dog_show.get_dog_count(show_id)
    page_count = math.ceil(dog_count / page_size)
    page_count = max(page_count, 1)
    dogs = dog_show.get_show_participants(show_id, page, page_size)

    if page < 1:
        return redirect(f"/dog_show/{show_id}/1")

    if page > page_count:
        return redirect(f"/dog_show/{show_id}/" + str(page_count))


    added_dogs = []
    eligible_dogs = []
    championship_titles = []
    if "owner_id" in session:
        owner_dogs = owner.get_dogs(session["owner_id"])
        added_dogs= dog_show.get_added_dogs(show_id, session["owner_id"])
        added_dog_ids = {d["id"] for d in added_dogs}
        eligible_dogs = [d for d in owner_dogs if d["id"] not in added_dog_ids]
        championship_titles = dog_show.get_championship_titles()

    return render_template("html/dog_show.html", show=show_info, dogs=dogs,
                           page=page, page_count=page_count, eligible_dogs=eligible_dogs,
                           added_dogs=added_dogs, championship_titles=championship_titles)

@app.route("/dog_show/<int:show_id>/add", methods=["POST"])
def add_dog_to_show(show_id):
    require_login()
    check_csrf()
    form = input_validator.get_dog_show_form(request)
    if not input_validator.check_dog_show_form(form):
        return redirect(f"/dog_show/{show_id}")

    dog_show.add_participant(show_id, form["dog_id"]
                                 , form["championship_title_id"])
    flash("Dog added to show successfully!", "success")
    return redirect(f"/dog_show/{show_id}")


@app.route("/dog_show/<int:show_id>/remove", methods=["POST"])
def remove_dog_from_show(show_id):
    require_login()
    check_csrf()
    form = input_validator.get_dog_show_form(request)
    if not input_validator.check_dog_show_form(form, True):
        return redirect(f"/dog_show/{show_id}")

    dog_show.remove_participant(form["show_id"], form["dog_id"])
    flash("Dog removed from show successfully!", "success")
    return redirect(f"/dog_show/{show_id}")


@app.route("/dog_shows")
@app.route("/dog_shows/<int:page>")
def show_dog_shows(page=1):
    page_size = 10
    dog_show_count = dog_show.get_dog_show_count()
    page_count = math.ceil(dog_show_count / page_size)
    page_count = max(page_count, 1)
    dog_shows = dog_show.get_dog_shows(page, page_size)

    if page < 1:
        return redirect("/dog_shows/1")

    if page > page_count:
        return redirect("/dog_shows/" + str(page_count))

    return render_template("html/dog_shows.html", page=page, page_count=page_count,
                           dog_shows=dog_shows)

def require_login():
    if "owner_id" not in session:
        abort(403, "ERROR: login required")

def require_owner(resource_owner_id):
    if session.get("owner_id") != resource_owner_id:
        abort(403, "ERROR: not allowed")

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403, "ERROR: invalid CSRF token")

def set_session(owner_id, name):
    session["owner_id"] = owner_id
    session["name"] = name
    session["csrf_token"] = secrets.token_hex(16)
