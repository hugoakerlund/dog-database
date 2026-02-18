import db

def get_dogs():
    sql = "SELECT * FROM dogs"
    return db.query(sql)

def get_breeds():
    sql = "SELECT * FROM DogBreeds"
    return db.query(sql)

