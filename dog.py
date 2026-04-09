import db

def get_dogs(page, page_size):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, "
        "d.date_of_birth, d.date_of_death, d.sex, d.owner_id, d.litter_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
        "l.name AS litter_name, "
        "o.name AS owner_name "
        "FROM Dogs d "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
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
        "SELECT d.id, d.registration_number, d.registration_date, d.name, d.image, "
        "d.color, d.breed, d.date_of_birth, d.date_of_death, d.sex, d.owner_id, "
        "d.litter_id, d.best_test, d.best_show_id, d.hip_index, d.use_index, "
        "l.name AS litter_name, "
        "o.name AS owner_name, "
        "s.name AS best_show_name "
        "FROM Dogs d "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Dog_shows s ON d.best_show_id = s.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
        "WHERE d.id = ?"
    )
    result = db.query(sql, [dog_id])
    return result[0] if result else None

def get_dog_by_registration_number(registration_number):
    sql = (
        "SELECT d.id, d.registration_number, d.registration_date, d.name, d.image, "
        "d.color, d.breed, d.date_of_birth, d.date_of_death, d.sex, d.owner_id, "
        "d.litter_id, d.best_test, d.best_show_id, d.hip_index, d.use_index, "
        "l.name AS litter_name, "
        "o.name AS owner_name, "
        "s.name AS best_show_name "
        "FROM Dogs d "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Dog_shows s ON d.best_show_id = s.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
        "WHERE d.registration_number = ?"
    )
    result = db.query(sql, [registration_number])
    return result[0] if result else None

def get_owner_id(dog_id):
    sql = "SELECT owner_id FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return int(result[0][0]) if result else None

def get_championship_title_id(title):
    sql = "SELECT id FROM Championship_titles WHERE title = ?"
    result = db.query(sql, [title])
    return result[0][0] if result else None

def get_championship_titles(dog_id):
    sql = (
        "SELECT c.title AS name "
        "FROM Show_participants s "
        "LEFT JOIN Championship_titles c ON s.result = c.id "
        "WHERE s.dog_id = ?")
    result = db.query(sql, [dog_id])
    return result if result else None

def get_registration_number(dog_id):
    sql = "SELECT registration_number FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_dog_id_by_registration_number(registration_number):
    sql = "SELECT id FROM Dogs WHERE registration_number = ?"
    result = db.query(sql, [registration_number])
    return result[0][0] if result else None

def get_dog_id_by_comment(comment_id):
    sql = "SELECT dog_id FROM Comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0][0] if result else None

def get_show_name(show_id):
    sql = "SELECT name FROM Dog_shows WHERE id = ?"
    result = db.query(sql, [show_id])
    return result[0][0] if result else None

def get_comments(dog_id):
    sql = (
        "SELECT c.id, c.content, c.owner_id, "
        "o.name AS commenter, "
        "c.dog_id, c.date "
        "FROM Comments c "
        "LEFT JOIN Owners o ON c.owner_id = o.id "
        "WHERE dog_id = ?"
    )
    return db.query(sql, [dog_id])

def get_comment(comment_id):
    sql = (
        "SELECT c.id, c.content, c.owner_id, c.dog_id, c.date "
        "FROM Comments c "
        "WHERE id = ?"
    )
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def get_colors():
    sql = "SELECT id, name FROM Colors"
    return db.query(sql)

def get_breeds():
    sql = "SELECT id, name FROM Dog_breeds"
    return db.query(sql)

def get_owners_dogs(owner_id):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, "
        "d.breed, d.date_of_birth, d.date_of_death, d.sex, d.owner_id, "
        "d.litter_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
        "FROM Dogs d "
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
    if result[0][0] is None:
        return False
    return True

def delete_dog(dog_id):

    sql = "UPDATE Litters SET father_id = NULL WHERE father_id = ?"
    db.execute(sql, [dog_id])

    sql = "UPDATE Litters SET mother_id = NULL WHERE mother_id = ?"
    db.execute(sql, [dog_id])

    sql = "UPDATE Dog_shows SET winner_id = NULL WHERE winner_id = ?"
    db.execute(sql, [dog_id])

    sql = "DELETE FROM Show_participants where dog_id = ?"
    db.execute(sql, [dog_id])

    sql = "DELETE FROM Dogs WHERE id = ?"
    db.execute(sql, [dog_id])

def insert_dog(form):
    sql = (
        "INSERT INTO Dogs (registration_number, registration_date, name, image, "
        "color, breed, date_of_birth, date_of_death, sex, litter_id, owner_id, "
        "best_show_id, best_test, hip_index, use_index) "
        "VALUES (?, datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    params = [
        form["registration_number"],
        form["name"],
        form["image_data"],
        form["color"],
        form["breed"],
        form["date_of_birth"],
        form["date_of_death"],
        form["sex"],
        form["litter_id"],
        form["owner_id"],
        form["best_show_id"],
        form["best_test"],
        form["hip_index"],
        form["use_index"]
    ]
    db.execute(sql, params)

def insert_comment(form):
    sql = (
        "INSERT INTO Comments (content, owner_id, dog_id, date) "
        "VALUES (?, ?, ?, datetime('now', 'localtime'))"
    )
    params = [
        form["content"],
        form["owner_id"],
        form["dog_id"],
    ]
    db.execute(sql, params)

def remove_comment(comment_id):
    sql = "DELETE FROM Comments WHERE id = ?"
    db.execute(sql, [comment_id])

def update_comment(form):
    sql = (
        "UPDATE Comments SET content = ? "
        "WHERE id = ?"
    )
    params = [
        form["content"],
        form["comment_id"]
    ]
    db.execute(sql, params)

def update_dog(dog_id, form):
    sql = (
        "UPDATE Dogs SET registration_number = ?, name = ?, image = ?, color = ?, "
        "breed = ?, date_of_birth = ?, date_of_death = ?, sex = ?, litter_id = ?, "
        "owner_id = ?, best_show_id = ?, best_test = ?,  hip_index = ?, use_index = ? "
        "WHERE id = ?"
    )
    params = [
        form["registration_number"],
        form["name"],
        form["image_data"],
        form["color"],
        form["breed"],
        form["date_of_birth"],
        form["date_of_death"],
        form["sex"],
        form["litter_id"],
        form["owner_id"],
        form["best_show_id"],
        form["best_test"],
        form["hip_index"],
        form["use_index"],
        dog_id
    ]
    db.execute(sql, params)

def registration_number_exists(registration_number):
    sql = "SELECT id FROM Dogs WHERE registration_number = ?"
    result = db.query(sql, [registration_number])
    return bool(result)

def search(query):
    sql = (
        "SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, "
        "d.date_of_birth, d.date_of_death, d.sex, d.owner_id, d.litter_id, "
        "d.best_test, d.best_show_id, d.hip_index, d.use_index, "
        "l.name AS litter_name, "
        "o.name AS owner_name "
        "FROM Dogs d "
        "LEFT JOIN Litters l ON d.litter_id = l.id "
        "LEFT JOIN Owners o ON d.owner_id = o.id "
        "WHERE d.name LIKE ? OR d.registration_number LIKE ? OR d.breed LIKE ?"
    )
    like_query = f"%{query}%"
    return db.query(sql, [like_query, like_query, like_query])
