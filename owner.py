from flask import session
from dog import DOG_FIELDS
from litter import BASE_LITTER_QUERY
import db

def get_owner(owner_id):
    sql = """SELECT id, name, email, password_hash, created_at
             FROM owners WHERE id = ?"""
    result = db.query(sql, [owner_id])
    return result[0] if result else None

def get_owner_count():
    sql = "SELECT COUNT(*) FROM owners"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_owners(page, page_size):
    sql = """SELECT id, name, email, password_hash
             FROM owners ORDER BY name LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dogs(owner_id, sex=None):
    sql = f"""SELECT {DOG_FIELDS},
             l.name AS litter_name,
             o.name AS owner_name
             FROM dogs d
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             WHERE d.owner_id = ?"""
    if sex == "Male":
        sql += " AND d.sex = 'Male'"

    elif sex == "Female":
        sql += " AND d.sex = 'Female'"

    return db.query(sql, [owner_id])

def get_litters(owner_id):
    sql =  f"""{BASE_LITTER_QUERY}
              WHERE l.owner_id = ?"""
    return db.query(sql, [owner_id])

def get_comment_owner_id(comment_id):
    sql = "SELECT owner_id FROM comments WHERE id = ?"
    owner_id = db.query(sql, [comment_id])
    return owner_id[0][0]

def get_id_with_name(name):
    sql = "SELECT id FROM owners WHERE name = ?"
    owner_id = db.query(sql, [name])
    if not owner_id:
        return None
    return owner_id[0][0]

def get_account_info(owner_id):
    sql = "SELECT name, email FROM owners WHERE id = ?"
    result = db.query(sql, [owner_id])
    return result[0][0], result[0][1]

def get_password_hash(name):
    sql = "SELECT password_hash FROM owners WHERE name = ?"
    result = db.query(sql, [name])
    if not result:
        return None
    return result[0][0]

def insert_owner(form):
    sql = """INSERT INTO owners (name, email, password_hash, created_at)
             VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    db.execute(sql, [form["name"], form["email"], form["password_hash"]])

def name_exists(name):
    sql = "SELECT 1 FROM owners WHERE name = ?"
    result = db.query(sql, [name])
    return bool(result)

def email_exists(email):
    sql = "SELECT 1 FROM owners WHERE email = ?"
    result = db.query(sql, [email])
    return bool(result)

def is_owner_of_dog(owner_id, dog_id):
    sql = "SELECT 1 FROM dogs d WHERE d.owner_id = ? AND d.id = ?"
    result = db.query(sql, [owner_id, dog_id])
    return bool(result)

def remove_owner(owner_id):
    sql = "DELETE FROM owners WHERE id = ?"
    db.execute(sql, [owner_id])

def update_owner(form):
    sql = """UPDATE owners SET name = ?, email = ?, password_hash = ?
             WHERE id = ?"""
    db.execute(sql, [form["name"], form["email"], form["password_hash"], session["owner_id"]])
