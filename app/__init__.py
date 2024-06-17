from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
# from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config['DEBUG_TB_ENABLED'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True

    # toolbar = DebugToolbarExtension(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app
