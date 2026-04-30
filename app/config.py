from app.util import get_env_variable


def build_dsn(test: bool = False) -> str:
    if get_env_variable("DATABASE_URL"):
        return get_env_variable("DATABASE_URL")

    dialect = get_env_variable("DB_DIALECT", default="postgresql")
    user = get_env_variable("POSTGRES_USER", default="ors2user")
    password = get_env_variable("POSTGRES_PASSWORD", default="ors2")
    host = get_env_variable("POSTGRES_DB_HOST", default="db")
    port = get_env_variable("POSTGRES_PORT", default=5432)
    db = get_env_variable("POSTGRES_DB", default="ors2") + ("_test" if test else "")
    return f"{dialect}://{user}:{password}@{host}:{port}/{db}"


class Config:
    SECRET_KEY = get_env_variable("SECRET_KEY", default="OSF")
    FLASK_ENV = get_env_variable("FLASK_ENV", default="development")
    DEBUG = False
    TESTING = False
    LOG_LEVEL = get_env_variable("LOG_LEVEL", "info").upper()

    TALISMAN_FORCE_HTTPS = True

    ENV = get_env_variable("ENV", default="production")

    # SQLAlchemy
    LOCAL_DSN = build_dsn()
    SQLALCHEMY_DATABASE_URI = get_env_variable("DATABASE_URL", default=LOCAL_DSN)

    # Silence deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rate limit requests to namenlijst.rechtspraak.nl
    RATE_LIMIT = False if get_env_variable("RATE_LIMIT", default=True) == "false" else True


class DevelopmentConfig(Config):
    DEBUG = True
    TALISMAN_FORCE_HTTPS = False


class TestConfig(Config):
    TESTING = True

    TALISMAN_FORCE_HTTPS = False
    LOCAL_DSN = build_dsn(test=True)
    SQLALCHEMY_DATABASE_URI = get_env_variable("DATABASE_URL", default=LOCAL_DSN)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    TALISMAN_FORCE_HTTPS = True


def get_config(env: str | None = None) -> Config:
    if env is None:
        env = get_env_variable("ENV", default="production")

    if env == "production":
        return ProductionConfig()
    if env == "test":
        return TestConfig()

    return DevelopmentConfig()
