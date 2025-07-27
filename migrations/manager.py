import os
import importlib.util
from datetime import datetime
import psycopg2


class MigrationManager:
    def __init__(self, database_url, migrations_dir="migrations"):
        self.database_url = database_url
        self.migrations_dir = migrations_dir
        self.ensure_migrations_table()

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)

    def ensure_migrations_table(self):
        """Create migrations table if it doesn't exist"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id SERIAL PRIMARY KEY,
                        version VARCHAR(255) UNIQUE NOT NULL,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                conn.commit()

    def get_applied_migrations(self):
        """Get list of applied migrations"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version FROM schema_migrations ORDER BY version")
                return [row[0] for row in cur.fetchall()]

    def get_pending_migrations(self):
        """Get list of migrations that haven't been applied"""
        applied = set(self.get_applied_migrations())
        all_migrations = []

        if os.path.exists(self.migrations_dir):
            for filename in sorted(os.listdir(self.migrations_dir)):
                if (
                    filename.endswith(".py")
                    and not filename.startswith("__")
                    and filename != "manager.py"
                ):  # Exclude the manager file itself
                    version = filename[:-3]  # Remove .py extension
                    if version not in applied:
                        all_migrations.append(version)

        return all_migrations

    def create_migration(self, name):
        """Create a new migration file"""
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.py"
        filepath = os.path.join(self.migrations_dir, filename)

        template = f'''"""
Migration: {name}
Created: {datetime.now().isoformat()}
"""

def up(cur):
    """
    Apply the migration
    cur: database cursor
    """
    # Add your SQL commands here
    # Example:
    # cur.execute("""
    #     CREATE TABLE example (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(255) NOT NULL
    #     )
    # """)
    pass


def down(cur):
    """
    Rollback the migration
    cur: database cursor
    """
    # Add your rollback SQL commands here
    # Example:
    # cur.execute("DROP TABLE IF EXISTS example")
    pass
'''

        with open(filepath, "w") as f:
            f.write(template)

        print(f"Created migration: {filepath}")
        return filepath

    def run_migration(self, version):
        """Run a specific migration"""
        migration_path = os.path.join(self.migrations_dir, f"{version}.py")

        if not os.path.exists(migration_path):
            raise Exception(f"Migration file not found: {migration_path}")

        # Load the migration module
        spec = importlib.util.spec_from_file_location(version, migration_path)
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Run the migration
                    migration_module.up(cur)

                    # Record that this migration was applied
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)",
                        (version,),
                    )

                    conn.commit()
                    print(f"Applied migration: {version}")

                except Exception as e:
                    conn.rollback()
                    print(f"Error applying migration {version}: {e}")
                    raise

    def migrate(self):
        """Run all pending migrations"""
        pending = self.get_pending_migrations()

        if not pending:
            print("No pending migrations")
            return

        print(f"Found {len(pending)} pending migrations")

        for version in pending:
            self.run_migration(version)

        print("All migrations completed")

    def rollback(self, version):
        """Rollback a specific migration"""
        migration_path = os.path.join(self.migrations_dir, f"{version}.py")

        if not os.path.exists(migration_path):
            raise Exception(f"Migration file not found: {migration_path}")

        # Load the migration module
        spec = importlib.util.spec_from_file_location(version, migration_path)
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Run the rollback
                    migration_module.down(cur)

                    # Remove migration record
                    cur.execute(
                        "DELETE FROM schema_migrations WHERE version = %s",
                        (version,),
                    )

                    conn.commit()
                    print(f"Rolled back migration: {version}")

                except Exception as e:
                    conn.rollback()
                    print(f"Error rolling back migration {version}: {e}")
                    raise

    def status(self):
        """Show migration status"""
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()

        print("Migration Status:")
        print("================")

        if applied:
            print("\nApplied migrations:")
            for version in applied:
                print(f"  ✓ {version}")

        if pending:
            print("\nPending migrations:")
            for version in pending:
                print(f"  ○ {version}")

        if not applied and not pending:
            print("No migrations found")
