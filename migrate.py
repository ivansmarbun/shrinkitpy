#!/usr/bin/env python3
import os
import sys
from config import config
from migrations.manager import MigrationManager

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
Migration CLI tool for ShrinkItPy
Usage:
    python migrate.py create <name>    # Create a new migration
    python migrate.py migrate         # Run all pending migrations
    python migrate.py rollback <version>  # Rollback specific migration
    python migrate.py status          # Show migration status
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Get database URL from config
    env = os.environ.get("FLASK_ENV", "development")
    db_url = config[env].DATABASE_URL

    manager = MigrationManager(db_url)
    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py create <migration_name>")
            sys.exit(1)
        name = sys.argv[2]
        manager.create_migration(name)

    elif command == "migrate":
        manager.migrate()

    elif command == "rollback":
        if len(sys.argv) < 3:
            print("Usage: python migrate.py rollback <version>")
            sys.exit(1)
        version = sys.argv[2]
        manager.rollback(version)

    elif command == "status":
        manager.status()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
