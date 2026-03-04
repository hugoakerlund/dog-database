import db

def get_dogs():
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
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id"
    )
    return db.query(sql)

def get_dog(dog_id):
    sql = (
        "SELECT d.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number, "
        "l.name AS litter_name, "
        "o.username AS owner_username, "
        "c.title AS championship_title, "
        "s.name AS best_show_name "
        "FROM Dogs d "
        "LEFT JOIN Dogs f ON d.father_id = f.id "
        "LEFT JOIN Dogs m ON d.mother_id = m.id "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id "
        "LEFT JOIN Dog_shows s ON d.best_show_id = s.id "
        "LEFT JOIN Users o ON d.owner_id = o.id "
        "WHERE d.id = ?"
    )
    result = db.query(sql, [dog_id])
    return result[0] if result else None

def get_owner_id(dog_id):
    sql = "SELECT owner_id FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_championship_titles():
    sql = "SELECT * FROM Championship_titles"
    return db.query(sql)

def get_registration_number(dog_id):
    sql = "SELECT registration_number FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_show_name(show_id):
    sql = "SELECT name FROM Dog_shows WHERE id = ?"
    result = db.query(sql, [show_id])
    return result[0][0] if result else None

def get_breeds():
    sql = "SELECT * FROM Dog_breeds"
    return db.query(sql)

def get_owners_dogs(owner_id):
    sql = (
        "SELECT d.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number "
        "FROM Dogs d "
        "LEFT JOIN Dogs f ON d.father_id = f.id "
        "LEFT JOIN Dogs m ON d.mother_id = m.id "
        "WHERE d.owner_id = ?"
    )
    dogs = db.query(sql, [owner_id])
    return dogs

def get_image(dog_id):
    sql = "SELECT image FROM Dogs WHERE id = ?"
    image = db.query(sql, [dog_id])
    return image[0][0] if image else None

def has_image(dog_id):
    sql = "SELECT image FROM Dogs WHERE id = ?"
    image = db.query(sql, [dog_id])
    return bool(image and image[0][0])
