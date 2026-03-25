import db

def get_owner(owner_id):
    sql = (
          "SELECT id, name, email, password_hash "
          "FROM Owners WHERE id = ?"
    )
    result = db.query(sql, [owner_id])
    return result[0] if result else None

def get_owner_count():
    sql = "SELECT COUNT(*) FROM Owners"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_owners(page, page_size):
    sql = (
          "SELECT id, name, email, password_hash "
          "FROM Owners ORDER BY name LIMIT ? OFFSET ?"
    )
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dogs(owner_id):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, d.date_of_birth, "
        "d.date_of_death, d.sex, d.father_id, d.mother_id, d.owner_id, d.litter_id, d.championship_title_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
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

def get_male_dogs(owner_id):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, d.date_of_birth, "
        "d.date_of_death, d.sex, d.father_id, d.mother_id, d.owner_id, d.litter_id, d.championship_title_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
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
        "WHERE d.owner_id = ? AND d.sex = 'M'"
    )
    result = db.query(sql, [owner_id])
    return result

def get_female_dogs(owner_id):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, d.date_of_birth, "
        "d.date_of_death, d.sex, d.father_id, d.mother_id, d.owner_id, d.litter_id, d.championship_title_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
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
        "WHERE d.owner_id = ? AND d.sex = 'F'"
    )
    result = db.query(sql, [owner_id])
    return result

def get_litters(owner_id):
    sql = (
        "SELECT l.id, l.name, l.father_id, l.mother_id, "
        "l.date_of_birth, l.owner_id, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number, "
        "o.name AS owner_name "
        "FROM Litters l "
        "LEFT JOIN Dogs f ON l.father_id = f.id "
        "LEFT JOIN Dogs m ON l.mother_id = m.id "
        "LEFT JOIN Owners o ON l.owner_id = o.id "
        "WHERE l.owner_id = ?"
    )
    result = db.query(sql, [owner_id])
    return result

def get_id_with_name(name):
    sql = "SELECT id FROM Owners WHERE name = ?"
    id = db.query(sql, [name])
    if not id:
        return None
    return id[0][0]

def get_password_hash(name):
    sql = "SELECT password_hash FROM Owners WHERE name = ?"
    result = db.query(sql, [name])
    if not result:
        return None
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

def is_owner_of_dog(owner_id, dog):
    sql = "SELECT id FROM Dogs d WHERE d.owner_id = ?"
    result = db.query(sql, [owner_id])
    return bool(result)
