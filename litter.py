from flask import session
import db

def get_litter(litter_id):
    sql = """SELECT l.id, l.name, l.father_id, l.mother_id,
             l.date_of_birth, l.owner_id,
             f.registration_number AS father_registration_number,
             m.registration_number AS mother_registration_number,
             o.name AS owner_name
             FROM Litters l
             LEFT JOIN Dogs f ON l.father_id = f.id
             LEFT JOIN Dogs m ON l.mother_id = m.id
             LEFT JOIN Owners o ON l.owner_id = o.id
             WHERE l.id = ?"""
    result = db.query(sql, [litter_id])
    return result[0]

def get_litter_count():
    sql = "SELECT COUNT(*) FROM Litters"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_litters(page, page_size):
    sql = """SELECT l.id, l.name, l.father_id, l.mother_id,
             l.date_of_birth, l.owner_id,
             f.registration_number AS father_registration_number,
             m.registration_number AS mother_registration_number,
             o.name AS owner_name
             FROM Litters l
             LEFT JOIN Dogs f ON l.father_id = f.id
             LEFT JOIN Dogs m ON l.mother_id = m.id
             LEFT JOIN Owners o ON l.owner_id = o.id
             GROUP BY l.id
             ORDER BY l.date_of_birth DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    result = db.query(sql, [limit, offset])
    return result

def get_dogs_in_litter(litter_id):
    sql = """SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed,
             d.date_of_birth, d.date_of_death, d.sex, d.owner_id, d.litter_id,
             d.best_test, d.best_show_id, d.hip_index, d.use_index,
             l.name AS litter_name,
             o.name AS owner_name
             FROM Dogs d
             LEFT JOIN Litters l ON d.litter_id = l.id
             LEFT JOIN Owners o ON d.owner_id = o.id
             WHERE d.litter_id = ?"""
    result = db.query(sql, [litter_id])
    return result

def insert_litter(form):
    sql = """INSERT INTO Litters (name, father_id, mother_id, date_of_birth, owner_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [form["name"], form["father_id"], form["mother_id"], form["date_of_birth"],
                     session["owner_id"]])

def update_litter(litter_id, form):
    sql = """UPDATE Litters
             SET name = ?, father_id = ?, mother_id = ?, date_of_birth = ?
             WHERE id = ?"""
    db.execute(sql, [form["name"], form["father_id"], form["mother_id"], form["date_of_birth"],
                     litter_id])

def delete_litter(litter_id):
    sql = "UPDATE Dogs SET litter_id = NULL WHERE litter_id = ?"
    db.execute(sql, [litter_id])

    sql = "DELETE FROM Litters WHERE id = ?"
    db.execute(sql, [litter_id])

def litter_name_exists(name):
    sql = "SELECT 1 FROM Litters WHERE name = ?"
    result = db.query(sql, [name])
    return bool(result)
