from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from datetime import datetime

    from app.assets import ensure_logo
    from app.routes import main_bp

    ensure_logo()
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    return app
