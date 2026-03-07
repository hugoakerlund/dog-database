from flask import session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import dog
import litter
import user

def check_registration_number(registration_number):
    if not len(registration_number) == 10 or \
       not registration_number.startswith("FI") or \
       not registration_number[2:7].isdigit() or \
       not registration_number[7] == "/" or \
       not registration_number[8:].isdigit():
        return False
    return True

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

def check_litter(litter_name):
    return len(litter_name) >= 2 and len(litter_name) <= 20 and \
           litter.get_litter_id_by_name(litter_name) is not None

def check_form_data(form):
    if not form["registration_number"] or not form["name"] or not form["breed"] or not \
        form["color"] or not form["date_of_birth"] or not form["sex"]:
        abort(400, "ERROR: registration number, name, breed, color, birth date, and sex are required")
    
    if not check_registration_number(form["registration_number"]):
        abort(400, "ERROR: invalid registration number format (must be 'FI12345/67')")

    if not check_name(form["name"]):
        abort(400, "ERROR: name must be between 2 and 20 characters")
    
    if not check_date(form["date_of_birth"]):
        abort(400, "ERROR: invalid birth date format (must be YYYY-MM-DD)")

    if form["date_of_death"] and not check_date(form["date_of_death"]):
        abort(400, "ERROR: invalid death date format (must be YYYY-MM-DD)")
    
    if form["father"] and not check_registration_number(form["father"]):
        abort(400, "ERROR: invalid father registration number format (must be 'FI12345/67')")

    if form["mother"] and not check_registration_number(form["mother"]):
        abort(400, "ERROR: invalid mother registration number format (must be 'FI12345/67')")
    
    if form["litter"] and not check_litter(form["litter"]):
        abort(400, "ERROR: invalid litter name (must be between 2 and 20 characters)")

    if not form["image"] or not form["image"].filename:
        abort(400, "ERROR: image is required")
    
    if not form["image"].filename.lower().endswith(('.jpg', '.jpeg')):
        abort(400, "ERROR: only .jpg and .jpeg images are allowed")

def get_dog_creation_form_data(request):
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
    form["father_dog_id"] = None
    form["mother"] = request.form.get("mother", "").strip() or None # Field is optional
    form["mother_dog_id"] = None
    form["litter"] = request.form.get("litter", "").strip() or None # Field is optional
    form["litter_id"] = None
    form["championship_title"] = request.form.get("championship_title", "").strip() or None
    form["owner_id"] = session["user_id"]

    if form["championship_title"]:
        form["championship_title_id"] = dog.get_championship_title_id(form["championship_title"])

    if form["father"]:
        form["father_dog_id"] = dog.get_dog_id_by_registration_number(form["father"])
        if not form["father_dog_id"]:
            abort(400, f"ERROR: father with registration number '{form['father']}' not found")
    
    if form["mother"]:
        form["mother_dog_id"] = dog.get_dog_id_by_registration_number(form["mother"])
        if not form["mother_dog_id"]:
            abort(400, f"ERROR: mother with registration number '{form['mother']}' not found")
    
    if form["litter"]:
        form["litter_id"] = litter.get_litter_id_by_name(form["litter"])
        if not form["litter_id"]:
            abort(400, f"ERROR: litter with name '{form['litter']}' not found")
    
    form["image_data"] = form["image"].read()
    if len(form["image_data"]) > 100 * 1024:
        abort(400, "ERROR: image size must be less than 100KB")
    
    check_form_data(form)
    return form

def check_litter_creation_form_data(form):
    if not form["name"] or not form["date_of_birth"] or not form["father_id"] or not form["mother_id"]:
        abort(400, "ERROR: All fields are required")
    
    if not check_name(form["name"]):
        abort(400, "ERROR: litter name must be between 2 and 20 characters")
    
    if not check_date(form["date_of_birth"]):
        abort(400, "ERROR: invalid birth date format (must be YYYY-MM-DD)")

    if  not check_registration_number(form["father"]):
        abort(400, "ERROR: invalid father registration number format (must be 'FI12345/67')")

    if not check_registration_number(form["mother"]):
        abort(400, "ERROR: invalid mother registration number format (must be 'FI12345/67')")

def get_litter_creation_form_data(request):
    form = {}
    form["name"] = request.form.get("name", "").strip()
    form["father"] = request.form.get("father", "").strip() or None
    form["father_id"] = dog.get_dog_id_by_registration_number(form["father"])
    form["mother"] = request.form.get("mother", "").strip() or None
    form["mother_id"] = dog.get_dog_id_by_registration_number(form["mother"])
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    check_litter_creation_form_data(form)
    return form

def check_registration_form_data(form):
    if not form["username"] or not form["email"] or not form["password1"] or not form["password2"]:
        abort(400, "ERROR: all fields are required")
    if form["password1"] != form["password2"]:
        abort(400, "ERROR: passwords do not match")
    if len(form["password1"]) < 8:
        abort(400, "ERROR: password must be atleast 8 characters long")
    if not check_name(form["username"]):
        abort(400, "ERROR: username must be between 2 and 20 characters")
    if not check_email(form["email"]):
        abort(400, "ERROR: invalid email address")
    form["password_hash"] = generate_password_hash(form["password1"])

def get_account_registration_form_data(request):
    form = {}
    form["username"] = request.form.get("username", "").strip()
    form["email"] = request.form.get("email", "").strip()
    form["password1"] = request.form.get("password1", "")
    form["password2"] = request.form.get("password2", "")
    check_registration_form_data(form)
    return form

def check_username(username):
    result = user.get_id_with_username(username)
    if not result:
        abort(400, "ERROR: Invalid username or password")
    return True

def check_email(email):
    return email.count("@") == 1 and email.count(".") == 1 and \
           email.index("@") < email.rindex(".") and email.index("@") > 0 and \
           email.rindex(".") < len(email) - 1

def check_password(password, username):
    result = user.get_password_hash(username) 
    if not result or not check_password_hash(result, password):
        abort(400, "ERROR: Invalid username or password")
    return True

def check_login(request):
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    check_username(username)
    check_password(password, username)
    user_id = user.get_id_with_username(username)
    return user_id, username