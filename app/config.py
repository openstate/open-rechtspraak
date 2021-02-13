from app.util import get_env_variable


def build_dsn(test=False):
    if get_env_variable("DATABASE_URL"):
        return get_env_variable("DATABASE_URL")

    dialect = get_env_variable("DB_DIALECT", default="postgresql")
    user = get_env_variable("DB_USER", default="ors2user")
    password = get_env_variable("DB_PASSWORD", default="ors2")
    host = get_env_variable("DB_HOST", default="db")
    port = get_env_variable("DB_PORT", default=5432)
    db = get_env_variable("DB_NAME", default="ors2") + ("_test" if test else "")
    return f"{dialect}://{user}:{password}@{host}:{port}/{db}"


class Config:
    SECRET_KEY = get_env_variable("SECRET_KEY", default="OSF")
    FLASK_ENV = get_env_variable("FLASK_ENV", default="development")
    DEBUG = False
    TESTING = False

    TALISMAN_FORCE_HTTPS = True

    ENV = get_env_variable("ENV", default="production")

    # SQLAlchemy
    LOCAL_DSN = build_dsn()
    SQLALCHEMY_DATABASE_URI = get_env_variable("DATABASE_URL", default=LOCAL_DSN)

    # Silence deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENTRY_DSN = get_env_variable("SENTRY_DSN", default="")
    SENTRY_CSP_REPORT_URI = get_env_variable("SENTRY_CSP_REPORT_URI", default="")


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
    pass


def get_config(env=None):
    if env is None:
        env = get_env_variable("ENV", default="production")

    if env == "production":
        return ProductionConfig()
    elif env == "test":
        return TestConfig()

    return DevelopmentConfig()
