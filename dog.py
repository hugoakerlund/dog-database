import db

def get_dogs():
    sql = "SELECT * FROM dogs"
    return db.query(sql)

def get_breeds():
    sql = "SELECT * FROM DogBreeds"
    return db.query(sql)

def get_owners_dogs(owner_id):
    sql = "SELECT * FROM Dogs WHERE owner_id = ?"
    dogs = db.query(sql, [owner_id])
    return dogs

