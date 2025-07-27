# ShrinkItPy URL Shortener

A Flask-based URL shortener with analytics, PostgreSQL database storage, and comprehensive CI/CD pipeline. The project follows Flask best practices with a modular structure for maintainability and scalability.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 12+ (or use Docker Compose)
- Docker & Docker Compose (optional)

### Development Setup

1. **Clone and setup environment**:
   ```bash
   git clone <repository-url>
   cd shrinkitpy
   cp .env.example .env
   # Edit .env with your database credentials
   ```

2. **Option A: Using Docker Compose (Recommended)**:
   ```bash
   docker-compose up -d
   # App will be available at http://localhost:5000
   ```

3. **Option B: Local Development**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Start PostgreSQL (ensure it's running)
   # Create database: createdb shrinkitpy_dev
   
   # Run migrations
   python migrate.py migrate
   
   # Start the app
   python app.py
   ```

## 🏗️ Architecture & Features

### Core Features
- **URL Shortening**: Convert long URLs to short, shareable links
- **Analytics**: Track URL usage and creation timestamps
- **RESTful API**: JSON API endpoints for programmatic access
- **Web Interface**: User-friendly forms for manual URL management
- **Database Migrations**: Version-controlled schema changes

### Technology Stack
- **Backend**: Flask (Python 3.12)
- **Database**: PostgreSQL with psycopg2 driver
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions with automated testing and Docker builds
- **Code Quality**: Black, Ruff, Flake8 with pre-commit hooks

## 📁 Project Structure
```
shrinkitpy/
├── app.py                 # Main Flask application
├── config.py              # Environment-based configuration
├── migrate.py             # Migration CLI tool
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Development environment
├── .env.example          # Environment variables template
├── services/             # Business logic layer
│   ├── db.py            # Database connection management
│   └── urls.py          # URL operations
├── migrations/           # Database migrations
│   ├── manager.py       # Migration system
│   └── *.py            # Individual migration files
├── templates/           # HTML templates
├── tests/              # Test suite
├── utils/              # Utility functions
└── .github/workflows/  # CI/CD pipeline
```

## 🔧 Database Management

### Migration System
The project includes a custom migration system for managing database schema changes:

```bash
# Create a new migration
python migrate.py create add_new_feature

# Run all pending migrations
python migrate.py migrate

# Check migration status
python migrate.py status

# Rollback a specific migration
python migrate.py rollback <migration_version>
```

### Database Configuration
Configure your database connection in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/shrinkitpy_dev
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py
```

## 🔍 Code Quality and Linting

This project uses multiple tools to ensure code quality:

### Linting Tools
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **Flake8**: Style guide enforcement

### Pre-commit Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run pre-commit on all files:
   ```bash
   pre-commit run --all-files
   ```

### Manual Code Quality Checks
```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Lint with Flake8
flake8 .
```

## 🚀 Deployment

### Docker Production Deployment
```bash
# Build production image
docker build -t shrinkitpy:latest .

# Run with environment variables
docker run -d \
  -p 5000:5000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e FLASK_ENV="production" \
  shrinkitpy:latest
```

### CI/CD Pipeline
The project includes a comprehensive GitHub Actions workflow that:
- Runs code quality checks (Black, Ruff, Flake8)
- Executes the test suite with PostgreSQL
- Builds and pushes Docker images to Docker Hub
- Supports multi-architecture builds (AMD64, ARM64)

## 📊 API Endpoints

### URL Shortening
```bash
# Shorten URL via API
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Analytics
```bash
# Get URL analytics
curl -X POST http://localhost:5000/analytics \
  -H "Content-Type: application/json" \
  -d '{"short_url": "abc123"}'
```

## 🔄 Migration from SQLite

If you're upgrading from the previous SQLite version:

1. **Backup your data**: Export existing URLs from SQLite
2. **Set up PostgreSQL**: Follow the setup instructions above
3. **Run migrations**: `python migrate.py migrate`
4. **Import data**: Use the migration system or manual SQL import

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and run tests: `pytest`
4. Run code quality checks: `pre-commit run --all-files`
5. Commit your changes: `git commit -m 'Add new feature'`
6. Push to the branch: `git push origin feature/new-feature`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Note**: This project was migrated from SQLite to PostgreSQL in July 2025. See [CHANGELOG.md](CHANGELOG.md) for detailed migration information.
├── templates/           # HTML templates
├── tests/              # Test suite
├── utils/              # Utility functions
└── .github/workflows/  # CI/CD pipeline
```

## 🔧 Database Management

### Migration System
The project includes a custom migration system for managing database schema changes:

```bash
# Create a new migration
python migrate.py create add_new_feature

# Run all pending migrations
python migrate.py migrate

# Check migration status
python migrate.py status

# Rollback a specific migration
python migrate.py rollback <migration_version>
```

### Database Configuration
Configure your database connection in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/shrinkitpy_dev
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py
```

## 🔍 Code Quality and Linting

This project uses multiple tools to ensure code quality:

### Linting Tools
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **Flake8**: Style guide enforcement

### Pre-commit Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install the pre-commit hook:
   ```bash
   pre-commit install
   ```
3. (Optional) Run pre-commit on all files:
   ```bash
   pre-commit run --all-files
   ```

Now, every time you commit, pre-commit will check and format your code automatically.

## Usage
- **Shorten URL:** Use the form on the homepage or POST to `/shorten` with JSON `{ "url": "LONG_URL" }`
- **Redirect:** Access `/s/SHORT_ID` to be redirected
- **Analytics:** Use the form at `/analytics` or POST to `/analytics` with JSON `{ "short_url": "SHORT_URL" }`

## Example curl
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"short_url": "http://localhost:5000/s/fOVDMX"}' \
    http://localhost:5000/analytics
```
