from datetime import datetime

from flask import Flask, jsonify, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config

db = SQLAlchemy()

PUBLIC_ENDPOINTS = frozenset({"auth.login", "auth.callback", "auth.logout", "static"})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)

    from app.assets import ensure_logo
    from app.auth import auth_bp, init_oauth, is_authenticated
    from app.routes import main_bp

    ensure_logo()
    init_oauth(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    if app.config.get("AUTH_ENABLED"):
        missing = [
            key
            for key in ("AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET")
            if not app.config.get(key)
        ]
        if missing:
            app.logger.warning(
                "AUTH_ENABLED is on but these Azure settings are missing: %s",
                ", ".join(missing),
            )

    @app.before_request
    def require_login():
        if not app.config.get("AUTH_ENABLED"):
            return None

        endpoint = request.endpoint or ""
        if endpoint in PUBLIC_ENDPOINTS or endpoint.startswith("static"):
            return None

        if is_authenticated():
            return None

        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized"}), 401

        return redirect(url_for("auth.login"))

    @app.context_processor
    def inject_globals():
        from app.access_log import is_log_admin

        return {
            "current_year": datetime.now().year,
            "auth_enabled": app.config.get("AUTH_ENABLED", False),
            "current_user": session.get("user"),
            "is_log_admin": is_log_admin(),
        }

    return app
