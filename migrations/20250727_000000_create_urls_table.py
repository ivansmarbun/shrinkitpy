"""
Migration: Create initial urls table
Created: 2025-07-27T00:00:00
"""


def up(cur):
    """
    Apply the migration
    cur: database cursor
    """
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            short_id VARCHAR(255) UNIQUE NOT NULL,
            long_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create index for faster lookups
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_urls_short_id ON urls(short_id)
    """
    )


def down(cur):
    """
    Rollback the migration
    cur: database cursor
    """
    cur.execute("DROP INDEX IF EXISTS idx_urls_short_id")
    cur.execute("DROP TABLE IF EXISTS urls")
