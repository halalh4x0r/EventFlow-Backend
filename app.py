from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config  # <-- import your config class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import your routes here later
    # from routes.events import events_bp
    # app.register_blueprint(events_bp)

    return app

app = create_app()
