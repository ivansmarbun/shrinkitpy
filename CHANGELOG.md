# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- PostgreSQL database support replacing SQLite
- Custom migration system for database schema management
- Environment-based configuration system (development, production, testing)
- Docker Compose setup for local development with PostgreSQL
- Comprehensive CI/CD pipeline with linting, testing, and Docker builds
- Support for multiple database environments

### Changed
- **BREAKING**: Migrated from SQLite to PostgreSQL
  - Updated database connection handling
  - Changed SQL syntax from SQLite to PostgreSQL
  - Added proper cursor management and connection pooling
- Updated Dockerfile to include PostgreSQL dependencies
- Enhanced GitHub Actions workflow with PostgreSQL service
- Improved test setup with database migration support

### Added Dependencies
- `psycopg2-binary==2.9.10` - PostgreSQL adapter for Python
- `python-dotenv==1.0.1` - Environment variable management

### Migration Guide
For existing installations:
1. Install new dependencies: `pip install -r requirements.txt`
2. Set up PostgreSQL database
3. Copy `.env.example` to `.env` and configure database URL
4. Run migrations: `python migrate.py migrate`

## [Previous] - Legacy SQLite Version
- Basic URL shortening functionality
- SQLite database storage
- Flask web interface
- Docker support
