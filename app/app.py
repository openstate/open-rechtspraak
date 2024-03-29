import sentry_sdk
from flask import Flask
from flask_talisman import Talisman
from sentry_sdk.integrations.flask import FlaskIntegration

from app import commands, seed
from app.api.routes import api_bp
from app.config import get_config
from app.core.routes import core_bp
from app.errors import internal_server_error, page_not_found, unauthorized_error
from app.extensions import cors, db, migrate, sitemap
from app.redirect.routes import redirect_bp
from app.util import get_env_variable


def create_app(env=None):
    initialize_sentry()
    app = Flask(__name__, static_folder="static")
    app.config.from_object(get_config(env))
    app.logger.setLevel(app.config["LOG_LEVEL"])
    flask_extensions(app)
    register_routes(app)
    register_commands(app)
    register_error_handlers(app)
    register_template_filters(app)
    return app


def flask_extensions(app):
    initialize_talisman(app)
    db.init_app(app)
    migrate.init_app(app, db)
    sitemap.init_app(app)
    cors.init_app(app)
    return None


def initialize_sentry():
    sentry_sdk.init(
        dsn=get_env_variable("SENTRY_DSN", default=""),
        integrations=[
            FlaskIntegration(),
        ],
        environment=get_env_variable("SENTRY_ENV", default="development"),
        traces_sample_rate=0.1,
        profiles_sample_rate=0.01,
    )


def initialize_talisman(app):
    SELF = "'self'"

    csp = {
        "default-src": [SELF],
        "style-src": [SELF],
        "script-src": [SELF, "analytics.openstate.eu"],
        "connect-src": [SELF, "analytics.openstate.eu"],
        "img-src": [SELF, "data:", "analytics.openstate.eu"],
        "font-src": [SELF],
        "base-uri": [],
        "object-src": [],
    }

    feature_policy = {
        "accelerometer": "'none'",
        "autoplay": "'none'",
        "camera": "'none'",
        "cross-origin-isolated": "'none'",
        "display-capture": "'none'",
        "document-domain": "'none'",
        "encrypted-media": "'none'",
        "fullscreen": "'none'",
        "geolocation": "'none'",
        "gyroscope": "'none'",
        "interest-cohort": "'none'",
        "magnetometer": "'none'",
        "microphone": "'none'",
        "midi": "'none'",
        "payment": "'none'",
        "picture-in-picture": "'none'",
        "publickey-credentials-get": "'none'",
        "screen-wake-lock": "'none'",
        "sync-xhr": "'none'",
        "usb": "'none'",
        "xr-spatial-tracking": "'none'",
    }

    permissions_policy = {
        "accelerometer": "()",
        "autoplay": "()",
        "camera": "()",
        "cross-origin-isolated": "()",
        "display-capture": "()",
        "document-domain": "()",
        "encrypted-media": "()",
        "fullscreen": "()",
        "geolocation": "()",
        "gyroscope": "()",
        "interest-cohort": "()",
        "magnetometer": "()",
        "microphone": "()",
        "midi": "()",
        "payment": "()",
        "picture-in-picture": "()",
        "publickey-credentials-get": "()",
        "screen-wake-lock": "()",
        "sync-xhr": "()",
        "usb": "()",
        "xr-spatial-tracking": "()",
    }

    app = Talisman(
        app,
        force_https=app.config["TALISMAN_FORCE_HTTPS"],
        content_security_policy=csp,
        content_security_policy_nonce_in=["script-src"],
        feature_policy=feature_policy,
        permissions_policy=permissions_policy,
        strict_transport_security=False,
    )
    return app


def register_error_handlers(app):
    app.register_error_handler(401, unauthorized_error)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)


def register_routes(app):
    app.register_blueprint(core_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(redirect_bp)


def register_commands(app):
    app.cli.add_command(commands.import_people)
    app.cli.add_command(commands.enrich_people)
    app.cli.add_command(commands.import_verdicts)
    app.cli.add_command(commands.enrich_verdicts)
    app.cli.add_command(commands.import_institutions)
    app.cli.add_command(commands.import_procedure_types)
    app.cli.add_command(commands.import_legal_areas)
    app.cli.add_command(commands.db_truncate)
    app.cli.add_command(seed.seed)


def register_template_filters(app):
    @app.template_filter("date")
    def _jinja2_filter_datetime(datetime):
        if datetime:
            return datetime.strftime("%d-%m-%Y")
        return ""

    return
