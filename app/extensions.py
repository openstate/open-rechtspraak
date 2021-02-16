from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sitemap import Sitemap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
sitemap = Sitemap()
