import db
from dog import DOG_FIELDS

LITTER_FIELDS = """
    l.id, l.name, l.father_id, l.mother_id,
    l.date_of_birth, l.owner_id"""

BASE_LITTER_QUERY = f"""
    SELECT {LITTER_FIELDS},
    f.registration_number AS father_registration_number,
    m.registration_number AS mother_registration_number,
    o.name AS owner_name
    FROM litters l
    LEFT JOIN dogs f ON l.father_id = f.id
    LEFT JOIN dogs m ON l.mother_id = m.id
    LEFT JOIN owners o ON l.owner_id = o.id"""

def get_litter(litter_id):
    sql = BASE_LITTER_QUERY + " WHERE l.id = ?"
    result = db.query(sql, [litter_id])
    return result[0]

def get_litter_count():
    sql = "SELECT COUNT(*) FROM litters"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_litters(page, page_size):
    sql = BASE_LITTER_QUERY + """
        ORDER BY l.date_of_birth DESC
        LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dogs_in_litter(litter_id):
    sql = f"""SELECT {DOG_FIELDS},
             l.name AS litter_name,
             o.name AS owner_name
             FROM dogs d
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             WHERE d.litter_id = ?"""
    return db.query(sql, [litter_id])

def insert_litter(form):
    sql = """INSERT INTO litters (name, father_id, mother_id, date_of_birth, owner_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [form["name"], form["father_id"], form["mother_id"], form["date_of_birth"],
                     form["owner_id"]])

def update_litter(litter_id, form):
    sql = """UPDATE litters
             SET name = ?, father_id = ?, mother_id = ?, date_of_birth = ?
             WHERE id = ?"""
    db.execute(sql, [form["name"], form["father_id"], form["mother_id"], form["date_of_birth"],
                     litter_id])

def delete_litter(litter_id):
    sql = "DELETE FROM litters WHERE id = ?"
    db.execute(sql, [litter_id])

def litter_name_exists(name):
    sql = "SELECT 1 FROM litters WHERE name = ?"
    result = db.query(sql, [name])
    return bool(result)
