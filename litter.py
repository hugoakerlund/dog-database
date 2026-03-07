import db

def get_litter(litter_id):
    sql = (
        "SELECT l.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number "
        "FROM Litters l "
        "LEFT JOIN Dogs f ON l.father_id = f.id "
        "LEFT JOIN Dogs m ON l.mother_id = m.id "
        "WHERE l.id = ?"
    )
    result = db.query(sql, [litter_id])
    return result[0] if result else None

def get_all_litters():
    sql = (
        "SELECT l.*, "
        "f.registration_number AS father_registration_number, "
        "m.registration_number AS mother_registration_number "
        "FROM Litters l "
        "LEFT JOIN Dogs f ON l.father_id = f.id "
        "LEFT JOIN Dogs m ON l.mother_id = m.id"
    )
    result = db.query(sql)
    return result

def get_litter_id_by_name(litter_name):
    sql = "SELECT id FROM Litters WHERE name = ?"
    result = db.query(sql, [litter_name])
    return result[0]["id"] if result else None

def get_dogs_in_litter(litter_id):
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
        "LEFT JOIN Championship_titles c ON d.championship_title_id = c.id "
        "WHERE d.litter_id = ?"
    )
    result = db.query(sql, [litter_id])
    return result

def insert_litter(form):
    sql = (
        "INSERT INTO Litters (name, father_id, mother_id, date_of_birth) "
        "VALUES (?, ?, ?, ?)"
    )
    db.execute(sql, [form["name"], form["father_id"], form["mother_id"], form["date_of_birth"]])