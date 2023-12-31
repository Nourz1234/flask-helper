import os

from .const import Environment
from .util import normalize_sqlalchemy_database_url, parse_bool


class BaseConfig:
    # General Config
    ENV: Environment = Environment.Development
    PORT = int(os.environ.get("PORT", "5000"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PREFERRED_URL_SCHEME = "http"

    # Debugging
    DEBUG = parse_bool(os.environ.get("DEBUG", "False"))
    TESTING = False
    EXPLAIN_TEMPLATE_LOADING = False

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = normalize_sqlalchemy_database_url(os.environ.get("DATABASE_URL", ""))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_SESSION_OPTIONS: dict = {"autoflush": False, "expire_on_commit": False}

    # Flask
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = None

    # Flask-Login
    REMEMBER_COOKIE_NAME = "remember_token"
    REMEMBER_COOKIE_DOMAIN = None
    REMEMBER_COOKIE_PATH = "/"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_SAMESITE = None


class BaseDevelopmentConfigMixIn:
    ENV = Environment.Development

    EXPLAIN_TEMPLATE_LOADING = True


class BaseProductionConfigMixIn:
    ENV = Environment.Production
    PREFERRED_URL_SCHEME = "https"

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
