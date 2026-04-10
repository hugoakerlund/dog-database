from flask import session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import dog
import litter
import owner
import dog_show

def get_dog_form(request):
    form = {}
    form["dog_id"] = request.form.get("dog_id", "").strip() or None
    form["registration_number"] = request.form.get("registration_number", "").strip()
    form["name"] = request.form.get("name", "").strip()
    form["image"] = request.files.get("image", "")
    form["image_data"] = None
    form["color"] = request.form.get("color", "").strip()
    form["breed"] = request.form.get("breed", "").strip()
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    form["date_of_death"] = request.form.get("date_of_death", "").strip() or None
    form["sex"] = request.form.get("sex", "").strip()
    form["litter_id"] = request.form.get("litter_id", "").strip() or None
    form["best_show_id"] = request.form.get("best_show_id", "").strip() or None
    form["best_test"] = request.form.get("best_test", "").strip() or None
    form["use_index"] = request.form.get("use_index", "").strip() or None
    form["hip_index"] = request.form.get("hip_index", "").strip() or None
    return form

def check_dog_form(form, edit=False):
    if not check_dog_required_fields(form):
        return False
    if not check_registration_number(form["registration_number"]):
        return False
    if edit:
        if not check_dog_edit_fields(form):
            return False
        if not check_registration_date(form):
            return False
    else:
        if dog.registration_number_exists(form["registration_number"]):
            flash("ERROR: registration number already exists!", "error")
            return False
    if not check_name(form["name"]):
        return False
    if not check_date(form["date_of_birth"]):
        return False
    if not check_sex(form):
        return False
    if not check_dog_optional_fields(form):
        return False
    return True

def check_dog_required_fields(form):
    if not form["registration_number"]:
        flash("ERROR: registration number is required!", "error")
        return False
    if not form["name"]:
        flash("ERROR: name is required!", "error")
        return False
    if not form["breed"]:
        flash("ERROR: breed is required!", "error")
        return False
    if not form["color"]:
        flash("ERROR: color is required!", "error")
        return False
    if not form["date_of_birth"]:
        flash("ERROR: date_of_birth is required!", "error")
        return False
    if not form["sex"]:
        flash("ERROR: sex is required!", "error")
        return False
    return True

def check_registration_number(registration_number):
    if not len(registration_number) == 10 or \
        not registration_number.startswith("FI") or \
        not registration_number[2:7].isdigit() or \
        not registration_number[7] == "/" or \
        not registration_number[8:].isdigit():
        flash("ERROR: invalid registration number format (must be 'FI12345/67')!", "error")
        return False
    return True

def check_dog_edit_fields(form):
    old_registration_number = dog.get_registration_number(form["dog_id"])
    if old_registration_number != form["registration_number"] and \
        dog.registration_number_exists(form["registration_number"]):
        flash("ERROR: registration number already exists!", "error")
        return False
    if not form["image"]:
        form["image_data"] = dog.get_image(form["dog_id"])
    return True

def check_registration_date(form):
    dog_data = dog.get_dog(form["dog_id"])
    if not dog_data:
        flash("ERROR: dog not found!", "error")
        return False

    registration_date = dog_data["registration_date"].split(' ')[0]
    date_of_birth  = form["date_of_birth"]

    year, month, day = registration_date.split("-")
    registration_date = date(int(year), int(month), int(day))

    year, month, day = date_of_birth.split("-")
    date_of_birth= date(int(year), int(month), int(day))

    if registration_date < date_of_birth:
        flash(f"ERROR: dog must be born before its registration date: {registration_date}!", "error")
        return False
    return True

def check_name(name):
    if (len(name) >= 2 and len(name) <= 20 and \
            all(c.isalpha() or c.isspace() for c in name)):
        return True
    flash("ERROR: name must be between 2 and 20 characters \
          and can only include letters and spaces!", "error")
    return False

def check_date(date_str):
    year, month, day = date_str.split("-")
    if not year.isdigit() or not month.isdigit() or not day.isdigit() or \
        not len(date_str) == 10 or not date_str[4] == "-" or not date_str[7] == "-":
        flash("ERROR: invalid date format (must be YYYY-MM-DD)!", "error")
        return False
    today = date.today()
    given_date = date(int(year), int(month), int(day))
    if today < given_date:
        flash("ERROR: date cannot be in the future!", "error")
        return False
    return True

def check_sex(form):
    if form["sex"] not in ["Male", "Female"]:
        flash("ERROR: invalid sex!", "error")
        return False
    return True

def check_dog_optional_fields(form):
    if form["image"] and not check_image(form):
        return False
    if form["date_of_death"] and not check_death_date(form["date_of_death"], form["date_of_birth"]):
        return False
    if form["litter_id"] and not check_litter(form["litter_id"]):
            return False
    if form["best_show_id"] and not check_best_show(form["best_show_id"]):
            return False
    if form["best_test"] and not check_test(form["best_test"]):
        return False
    if form["hip_index"] and not check_hip_index(form["hip_index"]):
        return False
    if form["use_index"] and not check_use_index(form["use_index"]):
        return False
    return True

def check_image(form):
    if not form["image"].filename.lower().endswith(('.jpg', '.jpeg')):
        flash("ERROR: only .jpg and .jpeg images are allowed!", "error")
        return False
    form["image_data"] = form["image"].read()
    if len(form["image_data"]) > 100 * 1024:
        flash("ERROR: image size must be less than 100KB!", "error")
        return False
    return True

def check_death_date(death_date_str, birth_date_str):
    if not check_date(death_date_str) or not check_date(birth_date_str):
        return False
    death_year, death_month, death_day = map(int, death_date_str.split("-"))
    birth_year, birth_month, birth_day = map(int, birth_date_str.split("-"))
    if (death_year, death_month, death_day) < (birth_year, birth_month, birth_day):
        flash("ERROR: invalid date of death!", "error")
        return False
    return True

def check_best_show(best_show_id):
    if not dog_show.get_dog_show(best_show_id):
        flash("ERROR: best show not found!", "error")
        return False
    return True

def check_litter(litter_id):
    owner_id = session["owner_id"]
    litter_father_id = litter.get_father_id(litter_id)
    litter_mother_id = litter.get_mother_id(litter_id)

    if not litter_father_id or not litter_mother_id:
        flash("ERROR: litters both parents could not be found!", "error")
        return False

    father_owner_id = dog.get_owner_id(litter_father_id)
    mother_owner_id = dog.get_owner_id(litter_mother_id)

    if owner_id == father_owner_id and owner_id == mother_owner_id:
        return True
    flash("ERROR: you are not the owner of the litter!", "error")
    return False

def check_test(score):
    try:
        val = int(score)
        if not 1 <= val <= 5:
            flash(f"ERROR: invalid best test '{score}' (must be between 1 and 5)!", "error")
            return False
    except ValueError:
        flash("ERROR: best test must be a number!", "error")
        return False
    return True

def check_hip_index(index):
    try:
        val = int(index)
        if not 1 <= val <= 100:
            flash(f"ERROR: invalid hip index '{index}' (must be between 1 and 100)!", "error")
            return False
    except ValueError:
        flash("ERROR: hip index must be a number!", "error")
        return False
    return True

def check_use_index(index):
    try:
        val = int(index)
        if not 1 <= val <= 100:
            flash(f"ERROR: invalid use index '{index}' (must be between 1 and 100)!", "error")
            return False
    except ValueError:
        flash("ERROR: use index must be a number!", "error")
        return False
    return True

def get_litter_form(request):
    form = {}
    form["litter_id"] = request.form.get("litter_id", "").strip() or None
    form["name"] = request.form.get("name", "").strip()
    form["father_id"] = request.form.get("father_id", "").strip() or None
    form["mother_id"] = request.form.get("mother_id", "").strip() or None
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    return form

def check_litter_form(form, edit=False):
    if not check_litter_required_fields(form):
        return False
    if not check_name(form["name"]):
        return False
    if not check_date(form["date_of_birth"]):
        return False
    if not check_father_and_mother(form):
        return False
    if edit:
        if not check_litter_edit_fields(form):
            return False
    elif litter.litter_name_exists(form["name"]):
        flash("ERROR: litter name already exists!", "error")
        return False
    return True

def check_litter_required_fields(form):
    if not form["name"]:
        flash("ERROR: name is required!", "error")
        return False
    if not form["date_of_birth"]:
        flash("ERROR: date of birth is required!", "error")
        return False
    if not form["father_id"]:
        flash("ERROR: father is required!", "error")
        return False
    if not form["mother_id"]:
        flash("ERROR: mother is required!", "error")
        return False
    return True

def check_litter_edit_fields(form):
    old_litter_name = litter.get_litter(form["litter_id"])["name"]
    if old_litter_name != form["name"] and litter.litter_name_exists(form["name"]):
        flash("ERROR: litter name already exists!", "error")
        return False
    return True

def check_father_and_mother(form):
    father_dog = dog.get_dog(form["father_id"])
    mother_dog = dog.get_dog(form["mother_id"])
    if not father_dog or not mother_dog:
        flash("ERROR: father or mother not found!", "error")
        return False
    if not check_father_and_mother_sex(father_dog, mother_dog):
        return False
    if not check_father_and_mother_date_of_birth(form["date_of_birth"],
                                                 mother_dog["date_of_birth"], father_dog["date_of_birth"]):
        return False
    if not check_ownership(form["father_id"]) or not check_ownership(form["mother_id"]):
        return False
    return True

def check_father_and_mother_sex(father_dog, mother_dog):
    if father_dog["sex"] == mother_dog["sex"]:
        flash("ERROR: father and mother cannot be same sex!", "error")
        return False
    return True

def check_father_and_mother_date_of_birth(litter_date_of_birth, father_date_of_birth, mother_date_of_birth):
    year, month, day = litter_date_of_birth.split("-")
    litter_date_of_birth = date(int(year), int(month), int(day))

    year, month, day = father_date_of_birth.split("-")
    father_date_of_birth = date(int(year), int(month), int(day))

    year, month, day = mother_date_of_birth.split("-")
    mother_date_of_birth = date(int(year), int(month), int(day))

    if litter_date_of_birth < mother_date_of_birth or litter_date_of_birth < father_date_of_birth:
        flash("ERROR: father and mother must be born before litter!", "error")
        return False
    return True

def check_ownership(parent_dog):
    owner_id = session["owner_id"]
    if not owner.is_owner_of_dog(owner_id, parent_dog):
        flash("ERROR: you are not the owner of both dogs!", "error")
        return False
    return True

def get_dog_show_form(request):
    form = {}
    form["dog_id"] = request.form.get("dog_id", "").strip()
    form["show_id"] = request.form.get("show_id", "").strip()
    form["championship_title_id"] = request.form.get("championship_title_id", "").strip() or None
    return form

def check_dog_show_form(form, remove=False):
    if not check_dog_show_dog(form):
        return False
    if not check_show_exists(form["show_id"]):
        return False
    if remove:
        if not dog_show.is_participant(form["show_id"], form["dog_id"]):
            flash("ERROR: dog is not registered for this show!", "error")
            return False
    else:
        if not check_dog_show_championship_title(form) or \
            not check_dog_aliveness(form) or \
            not check_dog_is_participant(form):
            return False
    return True

def check_dog_show_dog(form):
    if not form["dog_id"]:
        flash("ERROR: dog must be selected!", "error")
        return False
    try:
        form["dog_id"] = int(form["dog_id"])
    except ValueError:
        abort(400, "ERROR: invalid dog id")
    owner_id = session["owner_id"]
    owner_dog_ids = {d["id"] for d in owner.get_dogs(owner_id)}
    if form["dog_id"] not in owner_dog_ids:
        flash("ERROR: dog does not belong to you!", "error")
        return False
    return True

def check_show_exists(show_id):
    show_info = dog_show.get_dog_show(show_id)
    if not show_info:
        abort(404, "ERROR: dog show not found")
    return True

def check_dog_aliveness(form):
    if dog.is_dead(form["dog_id"]):
        flash("ERROR: cannot add dead dog to the show!", "error")
        return False
    return True

def check_dog_is_participant(form):
    if dog_show.is_participant(form["show_id"], form["dog_id"]):
        flash("ERROR: dog is already registered for this show!", "error")
        return False
    return True

def check_dog_show_championship_title(form):
    if not form["championship_title_id"]:
        flash("ERROR: show result must be selected!", "error")
        return False
    try:
        form["championship_title_id"]= int(form["championship_title_id"])
    except ValueError:
        abort(400, "ERROR: invalid championship title id")
    return True

def get_account_form(request):
    form = {}
    form["name"] = request.form.get("name", "").strip()
    form["email"] = request.form.get("email", "").strip()
    form["password1"] = request.form.get("password1", "")
    form["password2"] = request.form.get("password2", "")
    return form

def check_account_form(form, edit=False):
    if not check_account_required_fields(form):
        return False
    if not check_name(form["name"]):
        return False
    if not check_email(form["email"]):
        return False
    if not check_account_passwords(form):
        return False
    if edit:
        if not check_account_edit_fields(form):
            return False
    else:
        if owner.name_exists(form["name"]):
            flash("ERROR: name already taken!", "error")
            return False

        if owner.email_exists(form["email"]):
            flash("ERROR: email already taken!", "error")
            return False
    return True

def check_account_required_fields(form):
    if not form["name"] or not form["email"] or not form["password1"] or not form["password2"]:
        flash("ERROR: all fields are required!", "error")
        return False
    return True

def check_email(email):
    if email.count("@") == 1 and email.count(".") == 1 and \
        email.index("@") < email.rindex(".") and email.index("@") > 0 and \
        email.rindex(".") < len(email) - 1:
        return True
    flash("ERROR: invalid email address!", "error")
    return False

def check_account_passwords(form):
    if form["password1"] != form["password2"]:
        flash("ERROR: passwords do not match!", "error")
        return False
    if len(form["password1"]) < 8:
        flash("ERROR: password must be at least 8 characters long!", "error")
        return False
    form["password_hash"] = generate_password_hash(form["password1"])
    return True

def check_account_edit_fields(form):
    owner_id = session["owner_id"]
    old_account_name, old_email = owner.get_account_info(owner_id)
    if old_account_name != form["name"] and owner.name_exists(form["name"]):
        flash("ERROR: name already taken!", "error")
        return False
    if old_email != form["email"] and owner.email_exists(form["email"]):
        flash("ERROR: email already taken!", "error")
        return False
    return True

def get_comment_form(request, edit=False):
    form = {}
    if edit:
        form["comment_id"] = request.form.get("comment_id", "").strip()
        form["dog_id"] = dog.get_dog_id_by_comment(form["comment_id"])
    else:
        form["dog_id"] = request.form.get("dog_id", "").strip()
    form["content"] = request.form.get("content", "").strip()
    return form

def check_comment_form(form, edit=False ):
    if edit:
        if not check_comment_exists(form):
            return False
    if not check_comment_required_fieds(form):
        return False
    if not check_dog_exists(form):
        return False
    return True

def check_comment_required_fieds(form):
    if not form["dog_id"]:
        flash("ERROR: missing field dog_id!", "error")
        return False
    if not form["content"]:
        flash("ERROR: comment field cannot be empty!", "error")
        return False
    if len(form["content"]) > 5000:
        flash("ERROR: comment field cannot be longer than 5000 characters!", "error")
        return False
    return True

def check_dog_exists(form):
    if not dog.get_dog(form["dog_id"]):
        flash("ERROR: dog does not exist!", "error")
        return False
    return True

def check_comment_exists(form):
    if not form["comment_id"]:
        return False
    return True

def check_login(request):
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()
    owner_id = owner.get_id_with_name(name)
    if not check_password(password, name) or not owner_id:
        flash("ERROR: invalid name or password!", "error")
        return False
    return True

def check_password(password, name):
    result = owner.get_password_hash(name)
    if not result or not check_password_hash(result, password):
        return False
    return True
