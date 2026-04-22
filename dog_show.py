import db

def get_dog_show(show_id):
    sql = """SELECT s.id, s.name, s.winner_id, s.date, 
             d.registration_number AS winner_registration_number 
             FROM Dog_shows s 
             LEFT JOIN Dogs d ON s.winner_id = d.id 
             WHERE s.id = ?"""
    result = db.query(sql, [show_id])
    return result[0] if result else None

def get_show_participants(show_id):
    sql = """SELECT d.id, d.registration_number, d.name, d.image, d.color, d.breed, 
             d.date_of_birth, d.date_of_death, d.sex, d.owner_id, d.litter_id, 
             d.best_test, d.best_show_id, d.hip_index, d.use_index, 
             l.name AS litter_name, 
             o.name AS owner_name, 
             c.title AS show_result 
             FROM Dog_shows s 
             JOIN Show_participants pa ON s.id = pa.show_id 
             JOIN Dogs d ON pa.dog_id = d.id 
             LEFT JOIN Litters l ON d.litter_id = l.id 
             LEFT JOIN Owners o ON d.owner_id = o.id 
             LEFT JOIN Championship_titles c ON pa.result = c.id 
             WHERE s.id = ?"""
    return db.query(sql, [show_id])

def get_dog_shows(page, page_size):
    sql = """SELECT s.id, s.name, s.date 
             FROM Dog_shows s 
             ORDER BY s.id DESC 
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_championship_titles():
    sql = "SELECT id, title FROM Championship_titles"
    return db.query(sql)

def get_dog_show_count():
    sql = "SELECT COUNT(*) FROM Dog_shows"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_dog_participated_shows(dog_id):
    sql = """SELECT s.id, s.name, s.date, c.title AS show_result 
             FROM Dog_shows s 
             JOIN Show_participants sp ON s.id = sp.show_id 
             LEFT JOIN Championship_titles c on sp.result = c.id 
             WHERE sp.dog_id = ? ORDER BY s.date DESC"""
    return db.query(sql, [dog_id])

def is_participant(show_id, dog_id):
    sql = "SELECT 1 FROM Show_participants WHERE show_id = ? AND dog_id = ?"
    result = db.query(sql, [show_id, dog_id])
    return bool(result)


def add_participant(show_id, dog_id, championship_title_id):
    sql = "INSERT INTO Show_participants (show_id, dog_id, result) VALUES (?, ?, ?)"
    db.execute(sql, [show_id, dog_id, championship_title_id])


def remove_participant(show_id, dog_id):
    sql = "DELETE FROM Show_participants WHERE show_id = ? AND dog_id = ?"
    db.execute(sql, [show_id, dog_id])
