import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database Configuration
    DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://user:password@localhost:5432/shrinkitpy"
    
    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-please-change-in-production"
    
    # Environment
    ENV = os.environ.get("FLASK_ENV") or "development"
    DEBUG = ENV == "development"
    url = urlparse(DATABASE_URL)
    DATABASE_CONFIG = {
        "dbname": url.path[1:],
        "user": url.username,
        "password": url.password,
        "host": url.hostname,
        "port": url.port or 5432,
    }


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://user:password@localhost:5432/shrinkitpy_dev"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    TESTING = True
    DATABASE_URL = os.environ.get("TEST_DATABASE_URL") or "postgresql://user:password@localhost:5432/shrinkitpy_test"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
    "default": DevelopmentConfig,
}
