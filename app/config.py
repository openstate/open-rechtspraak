from app.util import get_env_variable

POSTGRES_URL = get_env_variable("POSTGRES_URL", default="db")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT", default="5432")
POSTGRES_USER = get_env_variable("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD", default="")
POSTGRES_DB = get_env_variable("POSTGRES_DB", default="stenos")


class Config:
    SECRET_KEY = get_env_variable("POSTGRES_DB", default="OSF")
    FLASK_ENV = get_env_variable("POSTGRES_URL", default="development")
    DEBUG = False
    TESTING = False

    ENV = get_env_variable("ENV", default="production")

    # SQLAlchemy
    LOCAL_DSN = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = get_env_variable("DATABASE_URL", default=LOCAL_DSN)

    # Silence deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # production config
    pass


def get_config(env=None):
    if env is None:
        env = get_env_variable("ENV", default="production")

    if env == "production":
        return ProductionConfig()
    elif env == "test":
        return TestConfig()

    return DevelopmentConfig()
