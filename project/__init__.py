import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()

def create_app(script_info=None):
    from project.models import models
    from project.scraper.views import scraper_blueprint

    # instantiate the app
    app = Flask(__name__, static_url_path='')

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

    # register the blueprints
    app.register_blueprint(scraper_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
