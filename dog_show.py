import db

def get_dog_show(show_id):
    sql = """SELECT s.id, s.name, s.winner_id, s.date,
             d.registration_number AS winner_registration_number
             FROM dog_shows s
             LEFT JOIN dogs d ON s.winner_id = d.id
             WHERE s.id = ?"""
    result = db.query(sql, [show_id])
    return result[0] if result else None

def get_dog_count(show_id):
    sql = """SELECT COUNT(*) FROM show_participants pa
             WHERE pa.show_id = ?"""
    result = db.query(sql, [show_id])
    return result[0][0] if result else 0

def get_show_participants(show_id, page, page_size):
    sql = """SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed,
             d.date_of_birth, d.date_of_death, d.sex, d.owner_id, d.litter_id,
             d.best_test, d.best_show_id, d.hip_index, d.use_index,
             l.name AS litter_name,
             o.name AS owner_name,
             c.title AS show_result
             FROM dog_shows s
             JOIN show_participants pa ON s.id = pa.show_id
             JOIN dogs d ON pa.dog_id = d.id
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             LEFT JOIN championship_titles c ON pa.result = c.id
             WHERE s.id = ?
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [show_id, limit, offset])

def get_added_dogs(show_id, owner_id):
    sql = """SELECT d.id, d.registration_number, d.name, d.breed,
             d.date_of_birth, d.sex, d.owner_id, d.litter_id,
             l.name AS litter_name,
             o.name AS owner_name,
             c.title AS show_result
             FROM dogs d
             LEFT JOIN show_participants pa ON d.id = pa.dog_id
             LEFT JOIN litters l ON d.litter_id = l.id
             LEFT JOIN owners o ON d.owner_id = o.id
             LEFT JOIN championship_titles c ON pa.result = c.id
             WHERE d.owner_id = ? AND pa.show_id = ?
             ORDER BY d.id DESC"""
    return db.query(sql, [owner_id, show_id])

def get_dog_shows(page, page_size):
    sql = """SELECT s.id, s.name, s.date
             FROM dog_shows s
             ORDER BY s.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_championship_titles():
    sql = "SELECT id, title FROM championship_titles"
    return db.query(sql)

def get_dog_show_count():
    sql = "SELECT COUNT(*) FROM dog_shows"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_dog_participated_shows(dog_id):
    sql = """SELECT s.id, s.name, s.date, c.title AS show_result
             FROM dog_shows s
             JOIN show_participants sp ON s.id = sp.show_id
             LEFT JOIN championship_titles c on sp.result = c.id
             WHERE sp.dog_id = ? ORDER BY s.date DESC"""
    return db.query(sql, [dog_id])

def is_participant(show_id, dog_id):
    sql = "SELECT 1 FROM show_participants WHERE show_id = ? AND dog_id = ?"
    result = db.query(sql, [show_id, dog_id])
    return bool(result)


def add_participant(show_id, dog_id, championship_title_id):
    sql = "INSERT INTO show_participants (show_id, dog_id, result) VALUES (?, ?, ?)"
    db.execute(sql, [show_id, dog_id, championship_title_id])


def remove_participant(show_id, dog_id):
    sql = "DELETE FROM show_participants WHERE show_id = ? AND dog_id = ?"
    db.execute(sql, [show_id, dog_id])
