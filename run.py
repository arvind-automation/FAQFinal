import os
import time

from app import create_app, db
from app.assets import ensure_logo
from app.db_init import initialize_database
from app.seed import seed_database

app = create_app()


def wait_for_db(max_retries=30, delay=2):
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.engine.connect()
            return
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)


if __name__ == "__main__":
    ensure_logo()
    wait_for_db()
    with app.app_context():
        initialize_database()
        seed_database()

    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=debug)
