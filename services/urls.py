from .db import get_db


def save_url(short_id, long_url):
    db = get_db()
    db.execute(
        "INSERT INTO urls (short_id, long_url) VALUES (?, ?)",
        (short_id, long_url),
    )
    db.commit()


def get_long_url(short_id):
    db = get_db()
    cur = db.execute(
        "SELECT long_url FROM urls WHERE short_id = ?", (short_id,)
    )
    row = cur.fetchone()
    return row[0] if row else None


def get_analytics(short_id):
    db = get_db()
    cur = db.execute(
        "SELECT short_id, long_url FROM urls WHERE short_id = ?", (short_id,)
    )
    row = cur.fetchone()
    return row if row else None
