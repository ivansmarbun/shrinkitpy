from services.db import get_db_connection 


def save_url(short_id, long_url):
    """Save a URL mapping to the database"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO urls (short_id, long_url) VALUES (%s, %s)",
            (short_id, long_url),
        )
        conn.commit()


def get_long_url(short_id):
    """Get the original URL from a short ID"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT long_url FROM urls WHERE short_id = %s", (short_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None


def get_analytics(short_id):
    """Get analytics data for a short URL"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT short_id, long_url, created_at FROM urls WHERE short_id = %s", 
            (short_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None
