"""Smoke tests for auth guard behavior (no live Azure connection required)."""

import os

os.environ["AUTH_ENABLED"] = "1"
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import create_app


def test_unauthenticated_redirects_to_login():
    app = create_app()
    app.config.update(
        {
            "AUTH_ENABLED": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "AZURE_TENANT_ID": "test-tenant",
            "AZURE_CLIENT_ID": "test-client",
            "AZURE_CLIENT_SECRET": "test-secret",
            "TESTING": True,
        }
    )

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 302
        assert "/login" in response.location


def test_api_returns_401_without_session():
    app = create_app()
    app.config.update(
        {
            "AUTH_ENABLED": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "AZURE_TENANT_ID": "test-tenant",
            "AZURE_CLIENT_ID": "test-client",
            "AZURE_CLIENT_SECRET": "test-secret",
            "TESTING": True,
        }
    )

    with app.test_client() as client:
        response = client.post("/api/feedback", json={"helpful": True})
        assert response.status_code == 401
        assert response.get_json()["error"] == "Unauthorized"


def test_auth_disabled_allows_portal():
    app = create_app()
    app.config.update(
        {
            "AUTH_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
        }
    )

    with app.app_context():
        from app import db

        db.create_all()

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


if __name__ == "__main__":
    test_unauthenticated_redirects_to_login()
    test_api_returns_401_without_session()
    test_auth_disabled_allows_portal()
    print("All auth smoke tests passed.")
