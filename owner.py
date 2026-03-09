from flask import abort
import db


def get_owner(owner_id):
    sql = "SELECT * FROM Owners WHERE id = ?"
    result = db.query(sql, [owner_id])
    return result[0] if result else None

def get_owner_count():
    sql = "SELECT COUNT(*) FROM Owners"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_owners(page, page_size):
    sql = "SELECT * FROM Owners ORDER BY name LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dogs(owner_id):
    sql = (
        "SELECT d.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number, "
        "l.name AS litter_name, "
        "o.name AS owner_name, "
        "c.title AS championship_title "
        "FROM Dogs d "
        "LEFT JOIN Dogs f ON d.father_id = f.id "
        "LEFT JOIN Dogs m ON d.mother_id = m.id "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id "
        "WHERE d.owner_id = ?"
    )
    result = db.query(sql, [owner_id])
    return result

def get_name_with_id(id):
    sql = "SELECT name FROM Owners WHERE id = ?"
    name = db.query(sql, [id])
    if not name:
        abort(404, "ERROR: owner not found")
    return name

def get_id_with_name(name):
    sql = "SELECT id FROM Owners WHERE name = ?"
    id = db.query(sql, [name])
    if not id:
        abort(404, "ERROR: invalid name or password")
    return id[0][0]

def get_password_hash(name):
    sql = "SELECT password_hash FROM Owners WHERE name = ?"
    result = db.query(sql, [name])
    if not result:
        abort(404, "ERROR: invalid name or password")
    return result[0][0]

def insert_owner(form):
    sql = "INSERT INTO Owners (name, email, password_hash) VALUES (?, ?, ?)"
    db.execute(sql, [form["name"], form["email"], form["password_hash"]])

def name_exists(name):
    sql = "SELECT id FROM Owners WHERE name = ?"
    result = db.query(sql, [name])
    return bool(result)

def email_exists(email):
    sql = "SELECT id FROM Owners WHERE email = ?"
    result = db.query(sql, [email])
    return bool(result)