import sqlite3
import logging
from flask import g, abort

logging.basicConfig(filename="database.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger=logging.getLogger(__name__)


def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=None):
    if params is None:
        params = []
    try:
        con = get_connection()
        result = con.execute(sql, params)
        con.commit()
        g.last_insert_id = result.lastrowid
        con.close()

    except sqlite3.IntegrityError as e:
        logger.error(e)
        abort(500, "ERROR: Database error")

def last_insert_id():
    return g.last_insert_id

def query(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
