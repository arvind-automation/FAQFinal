import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://gcc_user:gcc_pass@localhost:3306/arvind_gcc",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "1") == "1"
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
    AZURE_REDIRECT_URI = os.getenv(
        "AZURE_REDIRECT_URI", "https://faq.arvindgcc.com/auth/callback"
    )

    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "1") == "1"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=int(os.getenv("SESSION_LIFETIME_HOURS", "8"))
    )

    _admin_emails_raw = os.getenv("LOG_ADMIN_EMAILS", "")
    LOG_ADMIN_EMAILS = [
        email.strip().lower()
        for email in _admin_emails_raw.split(",")
        if email.strip()
    ]
