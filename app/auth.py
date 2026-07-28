from urllib.parse import quote

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, current_app, redirect, session, url_for

from app.access_log import record_access_log

oauth = OAuth()
auth_bp = Blueprint("auth", __name__)


def init_oauth(app):
    oauth.init_app(app)

    if not app.config.get("AUTH_ENABLED"):
        return

    tenant_id = app.config["AZURE_TENANT_ID"]
    oauth.register(
        name="microsoft",
        client_id=app.config["AZURE_CLIENT_ID"],
        client_secret=app.config["AZURE_CLIENT_SECRET"],
        server_metadata_url=(
            f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
        ),
        client_kwargs={"scope": "openid profile email User.Read"},
    )


def is_authenticated():
    return bool(session.get("user"))


@auth_bp.route("/login")
def login():
    if not current_app.config.get("AUTH_ENABLED"):
        return redirect(url_for("main.index"))

    if is_authenticated():
        return redirect(url_for("main.index"))

    redirect_uri = current_app.config.get("AZURE_REDIRECT_URI") or url_for(
        "auth.callback", _external=True
    )
    return oauth.microsoft.authorize_redirect(redirect_uri)


@auth_bp.route("/auth/callback")
def callback():
    if not current_app.config.get("AUTH_ENABLED"):
        return redirect(url_for("main.index"))

    token = oauth.microsoft.authorize_access_token()
    user_info = token.get("userinfo")
    if not user_info:
        user_info = oauth.microsoft.userinfo()

    session.clear()
    session["user"] = {
        "email": user_info.get("email") or user_info.get("preferred_username", ""),
        "name": user_info.get("name", ""),
    }
    session.permanent = True

    record_access_log("login", session["user"])

    return redirect(url_for("main.index"))


@auth_bp.route("/logout")
def logout():
    if not current_app.config.get("AUTH_ENABLED"):
        return redirect(url_for("main.index"))

    session.clear()

    tenant_id = current_app.config.get("AZURE_TENANT_ID", "")
    post_logout = quote(url_for("main.index", _external=True), safe="")
    logout_url = (
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={post_logout}"
    )
    return redirect(logout_url)
