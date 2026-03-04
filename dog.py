import db

def get_dogs():
    sql = "SELECT * FROM dogs"
    return db.query(sql)

def get_owner_id(dog_id):
    sql = "SELECT owner_id FROM Dogs WHERE id = ?"
    result = db.query(sql, [dog_id])
    return result[0][0] if result else None

def get_championship_title(title_id):
    sql = "SELECT title FROM Championship_titles WHERE id = ?"
    result = db.query(sql, [title_id])
    return result[0][0] if result else None

def get_breeds():
    sql = "SELECT * FROM Dog_breeds"
    return db.query(sql)

def get_owners_dogs(owner_id):
    sql = "SELECT * FROM Dogs WHERE owner_id = ?"
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
