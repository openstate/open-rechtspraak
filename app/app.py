from flask import Flask
from flask_talisman import Talisman

from app import commands
from app.config import get_config
from app.errors import internal_server_error, page_not_found, unauthorized_error
from app.extensions import db, migrate, toolbar
from app.routes import base_bp


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
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
    toolbar.init_app(app)
    return None


def initialize_talisman(app):
    SELF = (
        "'self' 'unsafe-inline' 'unsafe-eval'"
        if app.config["FLASK_ENV"] == "development"
        else "'self'"
    )

    csp = {
        "default-src": [SELF],
        "style-src": [SELF, "fonts.googleapis.com", "unpkg.com"],
        "script-src": [SELF],
        "connect-src": [
            SELF,
            "www.google-analytics.com",
        ],
        "font-src": [SELF, "fonts.gstatic.com"],
    }
    app = Talisman(
        app,
        content_security_policy=csp,
        content_security_policy_nonce_in=["script-src"],
    )
    return app


def register_error_handlers(app):
    app.register_error_handler(401, unauthorized_error)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)


def register_routes(app):
    app.register_blueprint(base_bp)


def register_commands(app):
    app.cli.add_command(commands.placeholder)
    app.cli.add_command(commands.import_people)


def register_template_filters(app):
    return
