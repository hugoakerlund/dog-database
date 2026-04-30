import db

DOG_FIELDS = """
    d.id, d.registration_number, d.registration_date, d.name, d.image,
    d.color, d.breed, d.date_of_birth, d.date_of_death, d.sex, d.owner_id,
    d.litter_id, d.best_test, d.best_show_id, d.hip_index, d.use_index"""

def get_dogs(page, page_size):
    sql = f"""SELECT {DOG_FIELDS},
             l.name AS litter_name,
             o.name AS owner_name
             FROM dogs d
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             ORDER BY d.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_dog_count():
    sql = "SELECT COUNT(*) FROM dogs"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_dog(dog_id):
    sql = f"""SELECT {DOG_FIELDS},
             l.name AS litter_name,
             o.name AS owner_name,
             s.name AS best_show_name
             FROM dogs d
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN dog_shows s ON d.best_show_id = s.id
             LEFT JOIN owners o ON d.owner_id = o.id
             WHERE d.id = ?"""
    result = db.query(sql, [dog_id])
    return result[0] if result else None

def get_litter_birth_dates(dog_id):
    sql = """SELECT l.date_of_birth
             FROM litters l
             WHERE l.father_id = ? OR l.mother_id = ?"""
    result = db.query(sql, [dog_id, dog_id])
    return result if result else None

def get_owner_id(dog_id):
    sql = "SELECT owner_id FROM dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return int(result[0][0]) if result else None

def get_registration_number(dog_id):
    sql = "SELECT registration_number FROM dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_dog_id_by_comment(comment_id):
    sql = "SELECT dog_id FROM comments WHERE id = ?"
    result = db.query(sql, [comment_id])
    return result[0][0] if result else None

def get_participated_show_ids(dog_id):
    sql = "SELECT show_id FROM show_participants WHERE dog_id = ?"
    result = db.query(sql, [dog_id])
    return result[0] if result else None

def get_comments(dog_id):
    sql = """SELECT c.id, c.content, c.owner_id,
             o.name AS commenter,
             c.dog_id, c.sent_at
             FROM comments c
             LEFT JOIN owners o ON c.owner_id = o.id
             WHERE dog_id = ?"""
    return db.query(sql, [dog_id])

def get_comment(comment_id):
    sql = """SELECT c.id, c.content, c.owner_id, c.dog_id, c.sent_at
             FROM comments c
             WHERE id = ?"""
    result = db.query(sql, [comment_id])
    return result[0] if result else None

def get_colors():
    sql = "SELECT id, name FROM colors"
    return db.query(sql)

def get_breeds():
    sql = "SELECT id, name FROM dog_breeds"
    return db.query(sql)

def get_image(dog_id):
    sql = "SELECT image FROM dogs WHERE id = ?"
    image = db.query(sql, [dog_id])
    return image[0][0] if image else None

def delete_dog(dog_id):
    sql = "DELETE FROM dogs WHERE id = ?"
    db.execute(sql, [dog_id])

def insert_dog(form):
    sql = """INSERT INTO dogs (registration_number, registration_date, name, image,
             color, breed, date_of_birth, date_of_death, sex, litter_id, owner_id,
             best_show_id, best_test, hip_index, use_index)
             VALUES (?, datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
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
    sql = """INSERT INTO comments (content, owner_id, dog_id, sent_at)
             VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    params = [
        form["content"],
        form["owner_id"],
        form["dog_id"],
    ]
    db.execute(sql, params)

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def update_comment(form):
    sql = """UPDATE comments SET content = ?
             WHERE id = ?"""
    params = [
        form["content"],
        form["comment_id"]
    ]
    db.execute(sql, params)

def update_dog(form):
    sql = """UPDATE dogs SET registration_number = ?, name = ?, image = ?, color = ?,
             breed = ?, date_of_birth = ?, date_of_death = ?, sex = ?, litter_id = ?,
             owner_id = ?, best_show_id = ?, best_test = ?,  hip_index = ?, use_index = ?
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
        form["litter_id"],
        form["owner_id"],
        form["best_show_id"],
        form["best_test"],
        form["hip_index"],
        form["use_index"],
        form["dog_id"],
    ]
    db.execute(sql, params)

def registration_number_exists(registration_number):
    sql = "SELECT 1 FROM dogs WHERE registration_number = ?"
    result = db.query(sql, [registration_number])
    return bool(result)

def get_search_count(query):
    sql = """SELECT COUNT(*)
             FROM dogs d
             WHERE d.name LIKE ? OR d.registration_number LIKE ? OR d.breed LIKE ?"""
    like_query = f"%{query}%"
    result = db.query(sql, [like_query, like_query, like_query])
    return result[0][0] if result else 0

def search(query, page, page_size):
    sql = f"""SELECT {DOG_FIELDS},
             l.name AS litter_name,
             o.name AS owner_name
             FROM dogs d
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             WHERE d.name LIKE ? OR d.registration_number LIKE ? OR d.breed LIKE ?
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    like_query = f"%{query}%"
    return db.query(sql, [like_query, like_query, like_query, limit, offset])
