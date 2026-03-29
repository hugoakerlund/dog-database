from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import dog
import litter
import owner
import dog_show

def check_registration_number(registration_number):
    if not len(registration_number) == 10 or \
       not registration_number.startswith("FI") or \
       not registration_number[2:7].isdigit() or \
       not registration_number[7] == "/" or \
       not registration_number[8:].isdigit():
        return False
    return True

def check_sex(father, mother):
    father_id = dog.get_dog_id_by_registration_number(father)
    mother_id = dog.get_dog_id_by_registration_number(mother)
    if not father_id or not mother_id:
        return False

    father_dog = dog.get_dog(father_id)
    mother_dog = dog.get_dog(mother_id)
    if not father_dog or not mother_dog:
        return False

    return father_dog["sex"] != mother_dog["sex"]

def check_ownership(parent):
    owner_id = session["owner_id"]
    parent_id = dog.get_dog_id_by_registration_number(parent)
    return owner.is_owner_of_dog(owner_id, parent_id)

def check_litter_parents(litter_id, father_id, mother_id):
    litter_father_id = litter.get_father_id(litter_id)
    litter_mother_id = litter.get_mother_id(litter_id)
    return father_id == int(litter_father_id) and mother_id == int(litter_mother_id)

def check_name(name):
    return len(name) >= 2 and len(name) <= 20 and \
           all(c.isalpha() or c.isspace() for c in name)

def check_date(date_str):
    if not len(date_str) == 10 or date_str[4] != "-" or date_str[7] != "-":
        return False
    year, month, day = date_str.split("-")
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    return True
 
def check_death_date(death_date_str, birth_date_str):
    if not check_date(death_date_str) or not check_date(birth_date_str):
        return False
    death_year, death_month, death_day = map(int, death_date_str.split("-"))
    birth_year, birth_month, birth_day = map(int, birth_date_str.split("-"))
    if (death_year, death_month, death_day) < (birth_year, birth_month, birth_day):
        return False
    return True

def check_litter_name(litter_name):
    return len(litter_name) >= 2 and len(litter_name) <= 20 and \
           litter.get_litter_id_by_name(litter_name) is not None

def check_dog_form(form, edit, old_registration_number=None):
    if not form["registration_number"] or not form["name"] or not form["breed"] or not \
        form["color"] or not form["date_of_birth"] or not form["sex"]:
        flash("ERROR: registration number, name, breed, color, date of birth, and sex are required")
        return False
    if not check_registration_number(form["registration_number"]):
        flash("ERROR: invalid registration number format (must be 'FI12345/67')")
        return False
    if edit and old_registration_number != form["registration_number"] and dog.registration_number_exists(form["registration_number"]):
        flash("ERROR: registration number already exists")
        return False
    if not edit and  dog.registration_number_exists(form["registration_number"]):
        flash("ERROR: registration number already exists")
        return False
    if not check_name(form["name"]):
        flash("ERROR: name must be between 2 and 20 characters")
        return False
    if not check_date(form["date_of_birth"]):
        flash("ERROR: invalid date of birth format (must be YYYY-MM-DD)")
        return False
    if form["date_of_death"] and not check_death_date(form["date_of_death"], form["date_of_birth"]):
        flash("ERROR: invalid date of death")
        return False
    if form["sex"] not in ["Male", "Female"]:
        flash("ERROR: invalid sex")
        return False
    if form["father"] and not check_registration_number(form["father"]):
        flash("ERROR: invalid father registration number format (must be 'FI12345/67')")
        return False
    if form["mother"] and not check_registration_number(form["mother"]):
        flash("ERROR: invalid mother registration number format (must be 'FI12345/67')")
        return False
    if not form["image"] or not form["image"].filename:
        flash("ERROR: image is required")
        return False
    if not form["image"].filename.lower().endswith(('.jpg', '.jpeg')):
        flash("ERROR: only .jpg and .jpeg images are allowed")
        return False
    form["image_data"] = form["image"].read()
    if len(form["image_data"]) > 100 * 1024:
        flash("ERROR: image size must be less than 100KB")
        return False
    if form["father"]:
        form["father_id"] = dog.get_dog_id_by_registration_number(form["father"])
        if not form["father_id"]:
            flash(f"ERROR: father with registration number '{form['father']}' not found")
            return False
    if form["mother"]:
        form["mother_id"] = dog.get_dog_id_by_registration_number(form["mother"])
        if not form["mother_id"]:
            flash(f"ERROR: mother with registration number '{form['mother']}' not found")
            return False
    if form["litter"]:
        form["litter_id"] = litter.get_litter_id_by_name(form["litter"])
        if not form.get("mother") or not form.get("father"):
            flash("ERROR: if litter is given father and mother must also be given")
            return False
        form["father_id"] = dog.get_dog_id_by_registration_number(form["father"])
        form["mother_id"] = dog.get_dog_id_by_registration_number(form["mother"])
        if not form["father_id"] or not form["mother_id"]:
            flash("ERROR: father or mother registration number not found")
            return False
        if not check_litter_parents(form["litter_id"], form["father_id"], form["mother_id"]):
            flash("ERROR: father and mother are not the parents of litter")
            return False

    if form["best_show"]:
        form["best_show_id"] = dog_show.get_show_id_by_name(form["best_show"])
        if not form["best_show_id"]:
            flash(f"ERROR: best show '{form['best_show']}' not found")
            return False
    if form["best_test"]:
        try:
            val = int(form["best_test"])
            if not 1 <= val <= 5:
                flash(f"ERROR: invalid best test '{form['best_test']}' (must be between 1 and 5)")
                return False
        except ValueError:
            flash(f"ERROR: best test must be a number")
            return False
    if form["hip_index"]:
        try:
            val = int(form["hip_index"])
            if not 1 <= val <= 100:
                flash(f"ERROR: invalid hip index '{form['hip_index']}' (must be between 1 and 100)")
                return False
        except ValueError:
            flash(f"ERROR: hip index must be a number")
            return False
    if form["use_index"]:
        try:
            val = int(form["use_index"])
            if not 1 <= val <= 100:
                flash(f"ERROR: invalid use index '{form['use_index']}' (must be between 1 and 100)")
                return False
        except ValueError:
            flash(f"ERROR: use index must be a number")
            return False
    return True

def get_dog_form(request):
    form = {}
    form["registration_number"] = request.form.get("registration_number", "").strip()
    form["name"] = request.form.get("name", "").strip()
    form["image"] = request.files.get("image")
    form["color"] = request.form.get("color", "").strip()
    form["breed"] = request.form.get("breed", "").strip()
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    form["date_of_death"] = request.form.get("date_of_death", "").strip() or None # Field is optional
    form["sex"] = request.form.get("sex", "").strip()
    form["father"] = request.form.get("father", "").strip() or None # Field is optional
    form["father_id"] = None
    form["mother"] = request.form.get("mother", "").strip() or None # Field is optional
    form["mother_id"] = None
    form["litter"] = request.form.get("litter", "").strip() or None # Field is optional
    form["litter_id"] = None
    form["championship_title"] = request.form.get("championship_title", "").strip() or None
    if form["championship_title"]:
        form["championship_title_id"] = dog.get_championship_title_id(form["championship_title"])
    form["best_show"] = request.form.get("best_show", "").strip() or None
    form["best_show_id"] = None
    form["best_test"] = request.form.get("best_test", "").strip() or None
    form["use_index"] = request.form.get("use_index", "").strip() or None
    form["hip_index"] = request.form.get("hip_index", "").strip() or None
    form["owner_id"] = session["owner_id"]
    return form

def check_litter_form(form, edit=False, old_litter_name=None):
    if not form["name"] or not form["date_of_birth"] or not form["father_id"] or not form["mother_id"]:
        flash("ERROR: all fields are required")
        return False
    if not check_name(form["name"]):
        flash("ERROR: litter name must be between 2 and 20 characters and can only contain letters and spaces")
        return False
    if edit and old_litter_name != form["name"] and litter.litter_name_exists(form["name"]):
        flash("ERROR: litter name already exists")
        return False
    if not check_date(form["date_of_birth"]):
        flash("ERROR: invalid date of birth format (must be YYYY-MM-DD)")
        return False
    if  not check_registration_number(form["father"]):
        flash("ERROR: invalid father registration number format (must be 'FI12345/67')")
        return False
    if not check_registration_number(form["mother"]):
        flash("ERROR: invalid mother registration number format (must be 'FI12345/67')")
        return False
    if form["father"] == form["mother"]:
        flash("ERROR: father and mother cannot be same")
        return False
    if not check_sex(form["father"], form["mother"]):
        flash("ERROR: father and mother cannot be same sex")
        return False
    if not check_ownership(form["father"]):
        flash("ERROR: you are not the owner of the father")
        return False
    if not check_ownership(form["mother"]):
        flash("ERROR: you are not the owner of the mother")
        return False
    return True

def get_litter_form(request):
    form = {}
    form["name"] = request.form.get("name", "").strip()
    form["father"] = request.form.get("father", "").strip() or None
    form["father_id"] = dog.get_dog_id_by_registration_number(form["father"])
    form["mother"] = request.form.get("mother", "").strip() or None
    form["mother_id"] = dog.get_dog_id_by_registration_number(form["mother"])
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    form["owner_id"] = session["owner_id"]
    return form

def check_registration_form(form):
    if not form["name"] or not form["email"] or not form["password1"] or not form["password2"]:
        flash("ERROR: all fields are required")
        return False
    if form["password1"] != form["password2"]:
        flash("ERROR: passwords do not match")
        return False
    if len(form["password1"]) < 8:
        flash("ERROR: password must be atleast 8 characters long")
        return False
    if not check_name(form["name"]):
        flash("ERROR: name must be between 2 and 20 characters")
        return False
    if owner.name_exists(form["name"]):
        flash("ERROR: name already taken")
        return False
    if not check_email(form["email"]):
        flash("ERROR: invalid email address")
        return False
    if owner.email_exists(form["email"]):
        flash("ERROR: email already taken")
        return False
    form["password_hash"] = generate_password_hash(form["password1"])
    return True

def get_registration_form(request):
    form = {}
    form["name"] = request.form.get("name", "").strip()
    form["email"] = request.form.get("email", "").strip()
    form["password1"] = request.form.get("password1", "")
    form["password2"] = request.form.get("password2", "")
    return form

def check_email(email):
    return email.count("@") == 1 and email.count(".") == 1 and \
           email.index("@") < email.rindex(".") and email.index("@") > 0 and \
           email.rindex(".") < len(email) - 1

def check_password(password, name):
    result = owner.get_password_hash(name) 
    if not result or not check_password_hash(result, password):
        return False
    return True

def check_login(request):
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()
    owner_id = owner.get_id_with_name(name)
    if not check_password(password, name) or not owner_id:
        flash("ERROR: invalid name or password")
        return False
    return True
