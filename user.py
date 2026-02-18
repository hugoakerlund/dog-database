from flask import abort
import db

def get_user_with_id(id):
    sql = "SELECT username FROM Users WHERE id = ?"
    username = db.query(sql, [id])
    if not username:
        abort(404)
    return username

def get_id_with_username(username):
    sql = "SELECT id FROM Users WHERE username = ?"
    id = db.query(sql, [username])
    if not id:
        abort(404)
    return id
