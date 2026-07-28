"""Create and update database schema to match SQLAlchemy models."""

import logging

from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn

from app import db

logger = logging.getLogger(__name__)


def _ensure_models_loaded():
    import app.models  # noqa: F401


def _sync_missing_columns():
    inspector = inspect(db.engine)
    dialect = db.engine.dialect
    changes = []

    for table_name, table in sorted(db.metadata.tables.items()):
        if not inspector.has_table(table_name):
            continue

        existing_columns = {column["name"] for column in inspector.get_columns(table_name)}

        for column in table.columns:
            if column.name in existing_columns:
                continue

            column_ddl = str(CreateColumn(column).compile(dialect=dialect)).strip()
            sql = text(f"ALTER TABLE `{table_name}` ADD COLUMN {column_ddl}")
            db.session.execute(sql)
            changes.append(f"Added column {table_name}.{column.name}")

    if changes:
        db.session.commit()

    return changes


def _sync_missing_indexes():
    inspector = inspect(db.engine)
    changes = []

    for table_name, table in sorted(db.metadata.tables.items()):
        if not inspector.has_table(table_name):
            continue

        existing_indexes = {index["name"] for index in inspector.get_indexes(table_name)}

        for index in table.indexes:
            if not index.name or index.name in existing_indexes:
                continue

            columns = ", ".join(f"`{column.name}`" for column in index.columns)
            unique = "UNIQUE " if index.unique else ""
            sql = text(
                f"CREATE {unique}INDEX `{index.name}` ON `{table_name}` ({columns})"
            )
            db.session.execute(sql)
            changes.append(f"Added index {index.name} on {table_name}")

    if changes:
        db.session.commit()

    return changes


def initialize_database():
    """Create missing tables and apply model changes to an existing database."""
    _ensure_models_loaded()

    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    model_tables = set(db.metadata.tables.keys())
    missing_tables = sorted(model_tables - existing_tables)

    db.create_all()

    column_changes = _sync_missing_columns()
    index_changes = _sync_missing_indexes()

    if missing_tables:
        logger.info("Created tables: %s", ", ".join(missing_tables))
        print(f"Created tables: {', '.join(missing_tables)}")

    for change in column_changes + index_changes:
        logger.info(change)
        print(change)

    if not missing_tables and not column_changes and not index_changes:
        print("Database schema is up to date.")

    return {
        "created_tables": missing_tables,
        "column_changes": column_changes,
        "index_changes": index_changes,
    }
