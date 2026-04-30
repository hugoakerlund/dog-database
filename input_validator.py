from datetime import date
from flask import session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import dog
import litter
import owner
import dog_show

def get_dog(request):
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
    form["owner_id"] = session["owner_id"]
    form["litter_id"] = request.form.get("litter_id", "").strip() or None
    form["best_show_id"] = request.form.get("best_show_id", "").strip() or None
    form["best_test"] = request.form.get("best_test", "").strip() or None
    form["use_index"] = request.form.get("use_index", "").strip() or None
    form["hip_index"] = request.form.get("hip_index", "").strip() or None
    return form

def validate_dog(form, edit=False):
    errors = []
    errors += check_dog_required_fields(form)

    if edit:
        errors += check_dog_edit_fields(form)
        errors += check_registration_date(form)

    else:
        if dog.registration_number_exists(form["registration_number"]):
            errors += ["ERROR: registration number already exists!"]

    errors += check_registration_number(form["registration_number"])
    errors += check_name(form["name"])
    errors += check_date(form["date_of_birth"])
    errors += check_sex(form)
    errors += check_dog_optional_fields(form)
    errors += check_dog_litters(form)
    errors += check_dog_shows(form)

    for e in errors:
        flash(e, "error")

    return len(errors) == 0

def check_dog_required_fields(form):
    errors = []
    if not form["registration_number"]:
        errors += ["ERROR: registration number is required!"]

    if not form["name"]:
        errors += ["ERROR: name is required!"]

    if not form["breed"]:
        errors += ["ERROR: breed is required!"]

    if not form["color"]:
        errors += ["ERROR: color is required!"]

    if not form["date_of_birth"]:
        errors += ["ERROR: date of birth is required!"]

    if not form["sex"]:
        errors += ["ERROR: sex is required!"]

    return errors

def check_registration_number(registration_number):
    errors = []
    if not len(registration_number) == 10 or \
        not registration_number.startswith("FI") or \
        not registration_number[2:7].isdigit() or \
        not registration_number[7] == "/" or \
        not registration_number[8:].isdigit():
        errors += ["ERROR: invalid registration number format (must be 'FI12345/67')!"]

    return errors

def check_dog_edit_fields(form):
    errors = []
    old_registration_number = dog.get_registration_number(form["dog_id"])
    if old_registration_number != form["registration_number"] and \
        dog.registration_number_exists(form["registration_number"]):
        errors += ["ERROR: registration number already exists!"]

    if not form["image"]:
        form["image_data"] = dog.get_image(form["dog_id"])

    return errors

def check_registration_date(form):
    errors = []
    dog_data = dog.get_dog(form["dog_id"])
    if not dog_data:
        errors += ["ERROR: dog not found!"]
        return errors

    registration_date = dog_data["registration_date"].split(" ")[0]
    registration_date = parse_date(registration_date)
    dog_date_of_birth = parse_date(form["date_of_birth"])
    if not registration_date or not dog_date_of_birth:
        return errors

    if registration_date < dog_date_of_birth:
        errors += [f"ERROR: dog must be born before its registration date: \
                       {registration_date}!"]

    return errors

def check_name(name):
    if len(name) >= 2 and len(name) <= 20 and \
        all(c.isalpha() or c.isspace() for c in name):
        return ""

    return ["ERROR: name must be between 2 and 20 characters \
          and can only include letters and spaces!"]

def check_date(date_str):
    errors = []
    given_date = parse_date(date_str)
    if not given_date:
        errors += ["ERROR: invalid date!"]
        return errors

    today = date.today()
    if today < given_date:
        errors += ["ERROR: date cannot be in the future!"]

    return errors

def check_sex(form):
    errors = []
    if form["sex"] not in ["Male", "Female"]:
        errors += ["ERROR: invalid sex!"]

    return errors

def check_dog_optional_fields(form):
    errors = []
    errors += process_image(form)
    errors += check_death_date(form)
    errors += check_litter(form)
    errors += check_best_show(form)
    errors += check_test(form)
    errors += check_hip_index(form)
    errors += check_use_index(form)
    return errors

def check_dog_litters(form):
    errors = []
    litters = dog.get_litter_birth_dates(form["dog_id"])
    if not litters:
        return errors

    dog_date_of_birth = parse_date(form["date_of_birth"])
    if not dog_date_of_birth:
        errors += ["ERROR: invalid dog date of birth!"]
        return errors

    for cur_litter in litters:
        litter_date_of_birth = parse_date(cur_litter["date_of_birth"])
        if not litter_date_of_birth:
            errors += ["ERROR: invalid litter date of birth!"]
            return errors

        if dog_date_of_birth > litter_date_of_birth:
            errors += ["ERROR: the dog has a litter whose date of birth is not \
                           possible with the dog's date of birth!"]

    return errors

def check_dog_shows(form):
    errors = []
    shows = dog.get_participated_show_ids(form["dog_id"])
    if shows:
        dog_date_of_birth = parse_date(form["date_of_birth"])
        if not dog_date_of_birth:
            errors += ["ERROR: invalid dog date of birth!"]
            return errors

        date_of_death = form["date_of_death"]
        if date_of_death:
            date_of_death = parse_date(date_of_death)

        for show_id in shows:
            show_info = dog_show.get_dog_show(show_id)
            if not show_info:
                abort(404, "ERROR: dog show not found")

            show_date = parse_date(show_info["date"])
            if not show_date:
                errors += ["ERROR: invalid show date!"]
                return errors

            if dog_date_of_birth > show_date:
                errors += ["ERROR: date of birth is not possible with the participated shows!"]

            if date_of_death and date_of_death < show_date:
                errors += ["ERROR: date of death is not possible with the participated shows!"]

    return errors

def process_image(form):
    errors = []
    if not form["image"]:
        return errors

    if not form["image"].filename.lower().endswith((".jpg", ".jpeg")):
        errors += ["ERROR: only .jpg and .jpeg images are allowed!"]

    form["image_data"] = form["image"].read()
    if len(form["image_data"]) > 100 * 1024:
        errors += ["ERROR: image size must be less than 100KB!"]

    return errors

def check_death_date(form):
    errors = []
    if not form["date_of_death"]:
        return errors

    date_of_death = parse_date(form["date_of_death"])
    date_of_birth = parse_date(form["date_of_birth"])
    if not date_of_birth or not date_of_death:
        errors += ["ERROR: invalid date!"]
        return errors

    if date_of_death < date_of_birth:
        errors += ["ERROR: date of death cannot be before date of birth!"]

    return errors

def check_best_show(form):
    errors = []
    if not form["best_show_id"]:
        return errors

    if not dog_show.get_dog_show(form["best_show_id"]):
        errors += ["ERROR: best show not found!"]

    return errors

def check_litter(form):
    errors = []
    if not form["litter_id"]:
        return errors

    litter_data = litter.get_litter(form["litter_id"])
    litter_father_id = litter_data["father_id"]
    litter_mother_id = litter_data["mother_id"]

    if not litter_father_id or not litter_mother_id:
        errors += ["ERROR: litter's both parents could not be found \
                       (one of them may have been deleted)!"]
        return errors

    if form["dog_id"] == litter_father_id or form["dog_id"] == litter_mother_id:
        errors += ["ERROR: a dog cannot be its litter's parent!"]

    father_owner_id = dog.get_owner_id(litter_father_id)
    mother_owner_id = dog.get_owner_id(litter_mother_id)

    owner_id = session["owner_id"]
    if owner_id != father_owner_id or owner_id != mother_owner_id:
        errors += ["ERROR: you are not the owner of the litter!"]

    litter_date_of_birth = litter_data["date_of_birth"]
    dog_date_of_birth = form["date_of_birth"]
    if litter_date_of_birth != dog_date_of_birth:
        errors += [f"ERROR: dog's date of birth ({dog_date_of_birth}) \
                    does not match the litter's date of birth ({litter_date_of_birth})!"]

    return errors

def check_test(form):
    errors = []
    if not form["best_test"]:
        return errors

    score = form["best_test"]
    try:
        val = int(score)
        if not 1 <= val <= 5:
            errors += [f"ERROR: invalid best test '{score}' (must be between 1 and 5)!"]

    except ValueError:
        errors += ["ERROR: best test must be a number!"]

    return errors

def check_hip_index(form):
    errors = []
    if not form["hip_index"]:
        return errors

    index = form["hip_index"]
    try:
        val = int(index)
        if not 1 <= val <= 100:
            errors += [f"ERROR: invalid hip index '{index}' (must be between 1 and 100)!"]

    except ValueError:
        errors += ["ERROR: hip index must be a number!"]

    return errors

def check_use_index(form):
    errors = []
    if not form["use_index"]:
        return errors

    index = form["use_index"]
    try:
        val = int(index)
        if not 1 <= val <= 100:
            errors += [f"ERROR: invalid use index '{index}' (must be between 1 and 100)!"]

    except ValueError:
        errors += ["ERROR: use index must be a number!"]

    return errors

def get_litter(request):
    form = {}
    form["litter_id"] = request.form.get("litter_id", "").strip() or None
    form["name"] = request.form.get("name", "").strip()
    form["father_id"] = request.form.get("father_id", "").strip() or None
    form["mother_id"] = request.form.get("mother_id", "").strip() or None
    form["owner_id"] = session["owner_id"]
    form["date_of_birth"] = request.form.get("date_of_birth", "").strip()
    return form

def validate_litter(form, edit=False):
    errors = []
    errors += check_litter_required_fields(form)
    errors += check_name(form["name"])
    errors += check_date(form["date_of_birth"])
    errors += check_father_and_mother(form)
    errors += check_litter_dogs(form)
    if edit:
        errors += check_litter_edit_fields(form)

    elif litter.litter_name_exists(form["name"]):
        errors += ["ERROR: litter name already exists!"]

    for e in errors:
        flash(e, "error")

    return len(errors) == 0

def check_litter_required_fields(form):
    errors = []
    if not form["name"]:
        errors += ["ERROR: name is required!"]

    if not form["date_of_birth"]:
        errors += ["ERROR: date of birth is required!"]

    if not form["father_id"]:
        errors += ["ERROR: father is required!"]

    if not form["mother_id"]:
        errors += ["ERROR: mother is required!"]

    return errors

def check_litter_edit_fields(form):
    errors = []
    old_litter_name = litter.get_litter(form["litter_id"])["name"]
    if old_litter_name != form["name"] and litter.litter_name_exists(form["name"]):
        errors += ["ERROR: litter name already exists!"]

    return errors

def check_father_and_mother(form):
    errors = []
    father_dog = dog.get_dog(form["father_id"])
    mother_dog = dog.get_dog(form["mother_id"])
    if not father_dog or not mother_dog:
        errors += ["ERROR: father or mother not found!"]
        return errors

    errors += check_father_and_mother_sex(father_dog, mother_dog)
    errors += check_parents_date_of_birth(form["date_of_birth"],
                                          mother_dog["date_of_birth"],
                                          father_dog["date_of_birth"])
    errors += check_ownership(form["father_id"])
    errors += check_ownership(form["mother_id"])
    return errors

def check_father_and_mother_sex(father_dog, mother_dog):
    errors = []
    if father_dog["sex"] == mother_dog["sex"]:
        errors += ["ERROR: father and mother cannot be same sex!"]

    return errors

def check_parents_date_of_birth(litter_date_of_birth, father_date_of_birth, mother_date_of_birth):
    errors = []
    litter_date_of_birth = parse_date(litter_date_of_birth)
    if not litter_date_of_birth:
        errors += ["ERROR: invalid litter date of birth!"]
        return errors

    father_date_of_birth = parse_date(father_date_of_birth)
    if not father_date_of_birth:
        errors += ["ERROR: invalid father date of birth!"]
        return errors

    mother_date_of_birth = parse_date(mother_date_of_birth)
    if not mother_date_of_birth:
        errors += ["ERROR: invalid mother date of birth!"]
        return errors

    if litter_date_of_birth < mother_date_of_birth or litter_date_of_birth < father_date_of_birth:
        errors += ["ERROR: father and mother must be born before litter!"]

    return errors

def check_ownership(parent_dog):
    errors = []
    owner_id = session["owner_id"]
    if not owner.is_owner_of_dog(owner_id, parent_dog):
        errors += ["ERROR: you are not the owner of both dogs!"]

    return errors

def check_litter_dogs(form):
    errors = []
    dogs = litter.get_dogs_in_litter(form["litter_id"])
    if not dogs:
        return errors

    litter_date_of_birth = parse_date(form["date_of_birth"])
    for cur_dog in dogs:
        dog_date_of_birth = parse_date(cur_dog["date_of_birth"])

        if dog_date_of_birth != litter_date_of_birth:
            errors += ["ERROR: the litter has a dog whose date of birth is not \
                           possible with the litter's date of birth!"]

    return errors

def get_dog_show(request):
    form = {}
    form["dog_id"] = request.form.get("dog_id", "").strip()
    form["show_id"] = request.form.get("show_id", "").strip()
    form["championship_title_id"] = request.form.get("championship_title_id", "").strip() or None
    return form

def validate_dog_show(form, remove=False):
    errors = []
    errors += check_dog_show_dog(form)
    errors += check_show_dates(form)
    if remove:
        if not dog_show.is_participant(form["show_id"], form["dog_id"]):
            errors += ["ERROR: dog is not registered for this show!"]

    else:
        errors +=  check_dog_show_championship_title(form)
        errors += check_dog_participation(form)

    for e in errors:
        flash(e, "error")

    return len(errors) == 0

def check_dog_show_dog(form):
    errors = []
    if not form["dog_id"]:
        errors += ["ERROR: dog must be selected!"]
        return errors

    try:
        form["dog_id"] = int(form["dog_id"])
    except ValueError:
        abort(400, "ERROR: invalid dog id")

    owner_id = session["owner_id"]
    if not owner.is_owner_of_dog(owner_id, form["dog_id"]):
        errors += ["ERROR: dog does not belong to you!"]

    return errors

def check_show_dates(form):
    errors = []
    show_info = dog_show.get_dog_show(form["show_id"])
    if not show_info:
        abort(404, "ERROR: dog show not found")

    dog_info = dog.get_dog(form["dog_id"])
    if not dog_info:
        errors += ["ERROR: dog could not be found!"]
        return errors

    if dog_info["date_of_death"]:
        errors += check_dog_death(dog_info, show_info)

    errors += check_dog_birth(dog_info, show_info)
    return errors

def check_dog_death(dog_info, show_info):
    errors = []
    show_date = parse_date(show_info["date"])
    date_of_death = parse_date(dog_info["date_of_death"])
    if not show_date or not date_of_death:
        errors += ["ERROR: invalid date!"]
        return errors

    if date_of_death < show_date:
        errors += ["ERROR: dog died before show!"]

    return errors

def check_dog_birth(dog_info, show_info):
    errors = []
    show_date = parse_date(show_info["date"])
    dog_date_of_birth = parse_date(dog_info["date_of_birth"])
    if not show_date or not dog_date_of_birth:
        errors += ["ERROR: invalid date!"]
        return errors

    if dog_date_of_birth > show_date:
        errors += ["ERROR: dog was born after show!"]

    return errors

def check_dog_participation(form):
    errors = []
    if dog_show.is_participant(form["show_id"], form["dog_id"]):
        errors += ["ERROR: dog is already registered for this show!"]

    return errors

def check_dog_show_championship_title(form):
    errors = []
    if not form["championship_title_id"]:
        errors += ["ERROR: show result must be selected!"]
        return errors

    try:
        form["championship_title_id"]= int(form["championship_title_id"])
    except ValueError:
        abort(400, "ERROR: invalid championship title id")

    return errors

def get_account(request):
    form = {}
    form["name"] = request.form.get("name", "").strip()
    form["email"] = request.form.get("email", "").strip()
    form["password1"] = request.form.get("password1", "")
    form["password2"] = request.form.get("password2", "")
    return form

def validate_account(form, edit=False):
    errors = []
    errors += check_account_required_fields(form)
    errors += check_name(form["name"])
    errors += check_email(form["email"])
    errors += process_account_passwords(form)
    if edit:
        errors += check_account_edit_fields(form)

    else:
        if owner.name_exists(form["name"]):
            errors += ["ERROR: name already taken!"]

        if owner.email_exists(form["email"]):
            errors += ["ERROR: email already taken!"]

    for e in errors:
        flash(e, "error")

    return len(errors) == 0

def check_account_required_fields(form):
    errors = []
    if not form["name"] or not form["email"] or not form["password1"] or not form["password2"]:
        errors += ["ERROR: all fields are required!"]

    return errors

def check_email(email):
    errors = []
    if "@" in email and "." in email and \
        email.index("@") < email.rindex(".") and email.index("@") > 0 and \
        email.rindex(".") < len(email) - 1:
        return errors

    errors += ["ERROR: invalid email address!"]
    return errors

def process_account_passwords(form):
    errors = []
    if form["password1"] != form["password2"]:
        errors += ["ERROR: passwords do not match!"]

    if len(form["password1"]) < 8:
        errors += ["ERROR: password must be at least 8 characters long!"]

    if len(form["password1"]) > 35:
        errors += ["ERROR: password cannot be longer than 35 characters!"]

    form["password_hash"] = generate_password_hash(form["password1"])
    return errors

def check_account_edit_fields(form):
    errors = []
    owner_id = session["owner_id"]
    old_account_name, old_email = owner.get_account_info(owner_id)
    if old_account_name != form["name"] and owner.name_exists(form["name"]):
        errors += ["ERROR: name already taken!"]

    if old_email != form["email"] and owner.email_exists(form["email"]):
        errors += ["ERROR: email already taken!"]

    return errors

def get_comment(request, edit=False):
    form = {}
    if edit:
        form["comment_id"] = request.form.get("comment_id", "").strip()
        form["dog_id"] = dog.get_dog_id_by_comment(form["comment_id"])

    else:
        form["dog_id"] = request.form.get("dog_id", "").strip()

    form["content"] = request.form.get("content", "").strip()
    form["owner_id"] = session["owner_id"]
    return form

def validate_comment(form, edit=False):
    errors = []
    if edit:
        errors += check_comment_exists(form)

    errors += check_comment_required_fields(form)
    errors += check_dog_exists(form)

    for e in errors:
        flash(e, "error")

    return len(errors) == 0

def check_comment_required_fields(form):
    errors = []
    if not form["dog_id"]:
        errors = ["ERROR: missing field dog_id!"]

    if not form["content"]:
        errors += ["ERROR: comment field cannot be empty!"]

    if len(form["content"]) > 5000:
        errors += ["ERROR: comment field cannot be longer than 5000 characters!"]

    return errors

def check_dog_exists(form):
    errors = []
    if not dog.get_dog(form["dog_id"]):
        errors +=  ["ERROR: dog does not exist!"]

    return errors

def check_comment_exists(form):
    errors = []
    if not form["comment_id"]:
        errors += ["ERROR: comment id is required!"]

    return errors

def check_login(request):
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "").strip()
    owner_id = owner.get_id_with_name(name)
    if not owner_id or not check_password(password, name):
        flash("ERROR: invalid name or password!", "error")
        return False

    return True

def check_password(password, name):
    result = owner.get_password_hash(name)
    if not result or not check_password_hash(result, password):
        return False

    return True

def parse_date(date_str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        flash("ERROR: invalid date!", "error")
        return None
