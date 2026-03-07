from flask import abort
import db


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

def insert_user(form):
    sql = "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)"
    db.execute(sql, [form["username"], form["email"], form["password_hash"]])