# Development Documentation

This document contains detailed information for developers working on ShrinkItPy.

## 🏗️ Architecture Overview

### Application Structure
ShrinkItPy follows a modular Flask architecture with clear separation of concerns:

```
Application Layers:
┌─────────────────┐
│   Web Routes    │  ← app.py (Flask routes and request handling)
├─────────────────┤
│  Business Logic │  ← services/ (URL operations, analytics)
├─────────────────┤
│  Data Access    │  ← services/db.py (Database abstraction)
├─────────────────┤
│   Database      │  ← PostgreSQL (Data persistence)
└─────────────────┘
```

### Key Components

#### 1. Configuration Management (`config.py`)
- Environment-based configuration (development, testing, production)
- Database URL management
- Secret key handling
- Environment variable loading

#### 2. Database Layer (`services/db.py`)
- PostgreSQL connection management
- Connection pooling via Flask's g object
- Cursor factory for dictionary-style results
- Proper connection cleanup

#### 3. Business Logic (`services/urls.py`)
- URL shortening operations
- Analytics data retrieval
- Database transaction management
- Error handling

#### 4. Migration System (`migrations/`)
- Version-controlled schema changes
- Forward and backward migration support
- CLI interface for migration management
- Automatic migration tracking

## 🔄 Migration System Deep Dive

### Migration File Structure
```python
"""
Migration: Description of changes
Created: ISO timestamp
"""

def up(cur):
    """Apply migration changes"""
    cur.execute("CREATE TABLE ...")

def down(cur):
    """Rollback migration changes"""
    cur.execute("DROP TABLE ...")
```

### Migration Naming Convention
`YYYYMMDD_HHMMSS_description.py`
- Timestamp ensures chronological ordering
- Descriptive name for easy identification
- Python file extension for importability

### Migration Best Practices
1. **Always provide rollback logic** in `down()` function
2. **Use transactions** - migrations are wrapped in database transactions
3. **Test migrations** on a copy of production data
4. **Keep migrations small** - easier to debug and rollback
5. **Document breaking changes** in migration comments

## 🗄️ Database Schema

### Current Schema (v1)

#### `urls` table
```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    short_id VARCHAR(255) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_urls_short_id ON urls(short_id);
```

#### `schema_migrations` table (system)
```sql
CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Planned Schema Extensions
Future migrations may include:
- Click tracking table
- User management
- URL expiration
- Analytics aggregation tables

## 🧪 Testing Strategy

### Test Structure
```
tests/
├── test_app.py          # Integration tests for Flask routes
├── test_urls.py         # Unit tests for URL service
├── test_migrations.py   # Migration system tests
└── conftest.py          # Pytest configuration and fixtures
```

### Testing Database
- Uses separate test database (`shrinkitpy_test`)
- Migrations run automatically before tests
- Database state isolated between test runs
- Proper cleanup after test completion

### Test Categories
1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Route and database interaction testing
3. **Migration Tests**: Schema change validation
4. **API Tests**: JSON endpoint validation

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
Workflow Steps:
1. Lint and Test Job:
   - Code formatting check (Black)
   - Linting (Ruff, Flake8)
   - Database migrations
   - Test execution with PostgreSQL

2. Build and Push Job:
   - Docker image building
   - Multi-architecture support
   - Image pushing to Docker Hub
   - Dependency on successful testing
```

### Quality Gates
- All linting checks must pass
- Test coverage requirements
- Migration validation
- Docker build success

### Deployment Strategy
- **Development**: Manual deployment from feature branches
- **Staging**: Automatic deployment from master branch
- **Production**: Tagged releases with manual approval

## 🔧 Development Workflow

### Setting Up Development Environment
1. **Clone repository**
2. **Create virtual environment**
3. **Install dependencies**
4. **Set up PostgreSQL**
5. **Configure environment variables**
6. **Run migrations**
7. **Start development server**

### Making Changes
1. **Create feature branch** from master
2. **Write tests** for new functionality
3. **Implement changes** following code standards
4. **Run quality checks** (linting, formatting)
5. **Execute test suite** locally
6. **Create migration** if schema changes needed
7. **Submit pull request**

### Code Standards
- **PEP 8** compliance enforced by Flake8
- **Black** formatting (line length: 79 characters)
- **Ruff** linting for code quality
- **Type hints** encouraged for new code
- **Docstrings** required for public functions

## 🐛 Debugging Guide

### Common Issues

#### Database Connection Errors
```python
# Check database URL format
DATABASE_URL=postgresql://user:password@host:port/database

# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check database exists
psql -l | grep shrinkitpy
```

#### Migration Failures
```bash
# Check migration status
python migrate.py status

# Rollback problematic migration
python migrate.py rollback <version>

# Fix migration file and retry
python migrate.py migrate
```

#### Docker Issues
```bash
# Check container logs
docker-compose logs app

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Logging Configuration
The application uses Flask's built-in logging. In development:
- Debug mode enabled
- Console output for errors
- Database query logging available

### Performance Monitoring
- Monitor database connection pool usage
- Track slow queries with PostgreSQL logs
- Use Docker stats for resource monitoring

## 📊 Metrics and Monitoring

### Application Metrics
- URL creation rate
- Redirection frequency
- Error rates
- Response times

### Database Metrics
- Connection pool utilization
- Query performance
- Index usage
- Storage growth

### Infrastructure Metrics
- Container resource usage
- Network latency
- Disk I/O patterns
- Memory consumption

## 🔒 Security Considerations

### Input Validation
- URL format validation
- SQL injection prevention (parameterized queries)
- XSS protection in templates
- CSRF token implementation (planned)

### Database Security
- Connection encryption in production
- Limited database user privileges
- Regular security updates
- Backup encryption

### Deployment Security
- Environment variable protection
- Container security scanning
- Regular dependency updates
- Secure communication protocols

## 📚 Additional Resources

### Flask Resources
- [Flask Best Practices](https://flask.palletsprojects.com/en/latest/patterns/)
- [Flask Testing](https://flask.palletsprojects.com/en/latest/testing/)
- [Flask Configuration](https://flask.palletsprojects.com/en/latest/config/)

### PostgreSQL Resources
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)
- [PostgreSQL Migrations](https://www.postgresql.org/docs/current/ddl-alter.html)

### Development Tools
- [Pre-commit Documentation](https://pre-commit.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
