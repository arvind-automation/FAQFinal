import logging
from urllib.parse import quote

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, current_app, redirect, request, session, url_for

from app.access_log import record_access_log

logger = logging.getLogger(__name__)

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
        client_kwargs={
            "scope": "openid profile email User.Read",
            "token_endpoint_auth_method": "client_secret_post",
        },
    )


def is_authenticated():
    return bool(session.get("user"))


def _redirect_uri():
    return current_app.config.get("AZURE_REDIRECT_URI") or url_for(
        "auth.callback", _external=True
    )


def _fetch_user_info():
    """Exchange auth code for tokens, then load profile without JWKS id_token validation."""
    oauth.microsoft.fetch_access_token(
        authorization_response=request.url,
        redirect_uri=_redirect_uri(),
    )

    try:
        return oauth.microsoft.userinfo()
    except Exception:
        logger.warning("userinfo endpoint failed, falling back to Microsoft Graph", exc_info=True)

    response = oauth.microsoft.get("https://graph.microsoft.com/v1.0/me")
    response.raise_for_status()
    profile = response.json()

    return {
        "email": profile.get("mail") or profile.get("userPrincipalName", ""),
        "name": profile.get("displayName", ""),
        "preferred_username": profile.get("userPrincipalName", ""),
    }


@auth_bp.route("/login")
def login():
    if not current_app.config.get("AUTH_ENABLED"):
        return redirect(url_for("main.index"))

    if is_authenticated():
        return redirect(url_for("main.index"))

    return oauth.microsoft.authorize_redirect(_redirect_uri())


@auth_bp.route("/auth/callback")
def callback():
    if not current_app.config.get("AUTH_ENABLED"):
        return redirect(url_for("main.index"))

    try:
        user_info = _fetch_user_info()
    except Exception:
        logger.exception("Microsoft SSO callback failed")
        session.clear()
        return redirect(url_for("auth.login"))

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
