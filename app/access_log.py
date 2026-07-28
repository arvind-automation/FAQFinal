from flask import current_app, request, session

from app import db
from app.models import AccessLog


def record_access_log(action: str, user: dict | None = None):
    user = user or session.get("user") or {}
    email = (user.get("email") or "unknown").strip().lower()
    name = (user.get("name") or "").strip()

    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip_address and "," in ip_address:
        ip_address = ip_address.split(",")[0].strip()

    user_agent = (request.headers.get("User-Agent") or "")[:512]

    entry = AccessLog(
        email=email,
        name=name,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.session.add(entry)
    db.session.commit()


def is_log_admin() -> bool:
    user = session.get("user")
    if not user:
        return False

    admin_emails = current_app.config.get("LOG_ADMIN_EMAILS", [])
    if not admin_emails:
        return False

    email = (user.get("email") or "").strip().lower()
    return email in admin_emails
