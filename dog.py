import db

def get_dogs(page, page_size):
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
        "GROUP BY d.id "
        "ORDER BY d.id DESC "
        "LIMIT ? OFFSET ?"
    )
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dog_count():
    sql = "SELECT COUNT(*) FROM Dogs"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_dog(dog_id):
    sql = (
        "SELECT d.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number, "
        "l.name AS litter_name, "
        "o.name AS owner_name, "
        "c.title AS championship_title, "
        "s.name AS best_show_name "
        "FROM Dogs d "
        "LEFT JOIN Dogs f ON d.father_id = f.id "
        "LEFT JOIN Dogs m ON d.mother_id = m.id "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id "
        "LEFT JOIN Dog_shows s ON d.best_show_id = s.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
        "WHERE d.id = ?"
    )
    result = db.query(sql, [dog_id])
    return result[0] if result else None

def get_owner_id(dog_id):
    sql = "SELECT owner_id FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_championship_title_id(title):
    sql = "SELECT id FROM Championship_titles WHERE title = ?"
    result = db.query(sql, [title])
    return result[0][0] if result else None

def get_championship_titles():
    sql = "SELECT * FROM Championship_titles"
    return db.query(sql)

def get_registration_number(dog_id):
    sql = "SELECT registration_number FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_dog_id_by_registration_number(registration_number):
    sql = "SELECT id FROM Dogs WHERE registration_number = ?"
    result = db.query(sql, [registration_number])
    return result[0][0] if result else None

def get_show_name(show_id):
    sql = "SELECT name FROM Dog_shows WHERE id = ?"
    result = db.query(sql, [show_id])
    return result[0][0] if result else None

def get_colors():
    sql = "SELECT * FROM Colors"
    return db.query(sql)

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

def is_dead(dog_id):
    sql = "SELECT date_of_death FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    if result[0][0] == None:
        return False
    return True

def delete_dog(dog_id):
    sql = "DELETE FROM Dogs WHERE id = ?"
    db.execute(sql, [dog_id])

def insert_dog(form):
        sql = """INSERT INTO Dogs (registration_number, name, image, color, breed, 
                                   date_of_birth, date_of_death, sex, father_id, mother_id, 
                                   litter_id, owner_id, championship_title_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        params = [
            form["registration_number"],
            form["name"],
            form["image_data"],
            form["color"],
            form["breed"],
            form["date_of_birth"],
            form["date_of_death"],
            form["sex"],
            form["father_dog_id"],
            form["mother_dog_id"],
            form["litter_id"],
            form["owner_id"],
            form["championship_title_id"]
        ]
        db.execute(sql, params)

def update_dog(dog_id, form):
    sql = """UPDATE Dogs 
             SET registration_number = ?, name = ?, image = ?, color = ?, breed = ?, 
                 date_of_birth = ?, date_of_death = ?, sex = ?, father_id = ?, mother_id = ?, 
                 litter_id = ?, owner_id = ?, championship_title_id = ?
             WHERE id = ?"""
    params = [
        form["registration_number"],
        form["name"],
        form["image_data"],
        form["color"],
        form["breed"],
        form["date_of_birth"],
        form["date_of_death"],
        form["sex"],
        form["father_dog_id"],
        form["mother_dog_id"],
        form["litter_id"],
        form["owner_id"],
        form["championship_title_id"],
        dog_id
    ]
    db.execute(sql, params)

def registration_number_exists(registration_number):
    sql = "SELECT id FROM Dogs WHERE registration_number = ?"
    result = db.query(sql, [registration_number])
    return bool(result)

def search(query):
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
        "WHERE d.name LIKE ? OR d.registration_number LIKE ? OR d.breed LIKE ?"
    )
    like_query = f"%{query}%"
    return db.query(sql, [like_query, like_query, like_query])