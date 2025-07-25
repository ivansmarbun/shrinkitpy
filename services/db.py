import sqlite3
from flask import g, current_app

DATABASE = "urls.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with current_app.app_context():
        db = get_db()
        db.execute(
            """CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_id TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        )"""
        )
        db.commit()


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
