from flask import abort
from werkzeug.security import check_password_hash
import db
import user


def get_user(user_id):
    sql = "SELECT * FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_users_dogs(user_id):
    sql = (
        "SELECT d.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number, "
        "l.name AS litter_name, "
        "o.username AS owner_username, "
        "c.title AS championship_title "
        "FROM Dogs d "
        "LEFT JOIN Dogs f ON d.father_id = f.id "
        "LEFT JOIN Dogs m ON d.mother_id = m.id "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Users o ON d.owner_id = o.id "
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id "
        "WHERE d.owner_id = ?"
    )
    result = db.query(sql, [user_id])
    return result

def get_username_with_id(id):
    sql = "SELECT username FROM Users WHERE id = ?"
    username = db.query(sql, [id])
    if not username:
        abort(404, "ERROR: user not found")
    return username

def get_id_with_username(username):
    sql = "SELECT id FROM Users WHERE username = ?"
    id = db.query(sql, [username])
    if not id:
        abort(404, "ERROR: invalid username or password")
    return id[0][0]

def get_password_hash(username):
    sql = "SELECT password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        abort(404, "ERROR: invalid username or password")
    return result[0][0]

def check_username(username):
    result = user.get_id_with_username(username)
    if not result:
        abort(400, "ERROR: Invalid username or password")
    return True

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
    return username, user_id