import psycopg2
import psycopg2.extras
from flask import g, current_app


def get_db_connection():
    """Get database connection from Flask g object"""
    db_config = current_app.config["DATABASE_CONFIG"]
    connection = psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"],
    )
    return connection


def init_db():
    with current_app.app_context():
        conn = current_app.config["DATABASE_CONFIG"]
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                short_id VARCHAR(255) UNIQUE NOT NULL,
                long_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
            )
            conn.commit()


def close_connection(exception):
    """Close database connection"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
