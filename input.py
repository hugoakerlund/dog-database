from flask import session, abort
import dog

def validate_registration_number(registration_number):
    if not len(registration_number) == 10 or \
       not registration_number.startswith("FI") or \
       not registration_number[2:7].isdigit() or \
       not registration_number[7] == "/" or \
       not registration_number[8:].isdigit():
        return False
    return True

def validate_name(name):
    return len(name) >= 2 and len(name) <= 20 and \
           all(c.isalpha() or c.isspace() for c in name)

def validate_date(date_str):
    if not len(date_str) == 10 or date_str[4] != "-" or date_str[7] != "-":
        return False
    year, month, day = date_str.split("-")
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    return True

def validate_email(email):
    return "@" in email and "." in email

def validate_form_data(form):
    if not form["registration_number"] or not form["name"] or not form["breed"] or not form["birth_date"] or not form["sex"]:
        abort(400, "ERROR: registration number, name, breed, birth date, and sex are required")
    
    if not validate_registration_number(form["registration_number"]):
        abort(400, "ERROR: invalid registration number format (must be 'FI12345/67')")

    if not validate_name(form["name"]):
        abort(400, "ERROR: name must be between 2 and 20 characters")
    
    if not validate_date(form["birth_date"]):
        abort(400, "ERROR: invalid birth date format (must be YYYY-MM-DD)")

    if form["death_date"] and not validate_date(form["death_date"]):
        abort(400, "ERROR: invalid death date format (must be YYYY-MM-DD)")
    
    if form["father"] and not validate_registration_number(form["father"]):
        abort(400, "ERROR: invalid father registration number format (must be 'FI12345/67')")

    if form["mother"] and not validate_registration_number(form["mother"]):
        abort(400, "ERROR: invalid mother registration number format (must be 'FI12345/67')")

    if not form["image"] or not form["image"].filename:
        abort(400, "ERROR: image is required")
    
    if not form["image"].filename.lower().endswith(('.jpg', '.jpeg')):
        abort(400, "ERROR: only .jpg and .jpeg images are allowed")

def get_form_data(request):
    form = {}
    form["registration_number"] = request.form.get("registration_number", "").strip()
    form["name"] = request.form.get("name", "").strip()
    form["image"] = request.files.get("image")
    form["color"] = request.form.get("color", "").strip()
    form["breed"] = request.form.get("breed", "").strip()
    form["birth_date"] = request.form.get("birth_date", "").strip()
    form["death_date"] = request.form.get("death_date", "").strip() or None # Field is optional
    form["sex"] = request.form.get("sex", "").strip()
    form["father"] = request.form.get("father", "").strip() or None # Field is optional
    form["mother"] = request.form.get("mother", "").strip() or None # Field is optional
    form["championship_title"] = request.form.get("championship_title", "").strip() or None
    form["owner_id"] = session["user_id"]

    if form["championship_title"]:
        form["championship_title_id"] = dog.get_championship_title_id(form["championship_title"])

    form["father_dog_id"] = None
    form["mother_dog_id"] = None
    if form["father"]:
        form["father_dog_id"] = dog.get_dog_id_by_registration_number(form["father"])
        if not form["father_dog_id"]:
            abort(400, f"ERROR: father with registration number '{form['father']}' not found")
    
    if form["mother"]:
        form["mother_dog_id"] = dog.get_dog_id_by_registration_number(form["mother"])
        if not form["mother_dog_id"]:
            abort(400, f"ERROR: mother with registration number '{form['mother']}' not found")
    
    form["image_data"] = form["image"].read()
    if len(form["image_data"]) > 100 * 1024:
        abort(400, "ERROR: image size must be less than 100KB")
    
    validate_form_data(form)
    return form