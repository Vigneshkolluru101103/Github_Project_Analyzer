"""
PostgreSQL database configuration for Supabase via SQLAlchemy.
"""

import logging
import os
import re
from collections.abc import Generator
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# Load backend/.env regardless of working directory
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH)

DATABASE_URL: str | None = os.getenv("DATABASE_URL")

engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None
Base = declarative_base()


def _sanitize_database_url(raw: str | None) -> str | None:
    """
    Normalize DATABASE_URL value from environment.
    Fixes common .env mistakes like duplicate 'DATABASE_URL=' prefix.
    """
    if not raw:
        return None

    value = raw.strip().strip('"').strip("'")

    # Handle: DATABASE_URL=postgresql://... (duplicate key pasted into value)
    if value.upper().startswith("DATABASE_URL="):
        value = value.split("=", 1)[1].strip()

    return value or None


def mask_database_url(url: str) -> str:
    try:
        parsed = make_url(url)
        return parsed.set(password="********").render_as_string(hide_password=False)
    except Exception:
        return re.sub(r":([^:@/]+)@", r":********@", url, count=1)


def detect_connection_type(host: str | None) -> str:
    """Identify Supabase connection mode from hostname."""
    if not host:
        return "Unknown"

    host_lower = host.lower()
    if "pooler.supabase.com" in host_lower:
        return "Session Pooler"
    if host_lower.startswith("db.") and host_lower.endswith(".supabase.co"):
        return "Direct Connection"
    return "Unknown"


def parse_database_url_info(url: str) -> dict:
    """
    Parse and validate a SQLAlchemy-compatible database URL.
    Raises ValueError with a clear message if the format is invalid.
    """
    if not url:
        raise ValueError("DATABASE_URL is empty")

    if not url.startswith(("postgresql://", "postgresql+psycopg2://")):
        raise ValueError(
            f"Invalid DATABASE_URL scheme. Expected 'postgresql://...' but got "
            f"'{url[:40]}...'. Check for a duplicate 'DATABASE_URL=' prefix in .env"
        )

    try:
        parsed = make_url(url)
    except ArgumentError as exc:
        raise ValueError(f"SQLAlchemy could not parse DATABASE_URL: {exc}") from exc

    host = parsed.host or ""
    connection_type = detect_connection_type(host)
    if "pooler.supabase.com" in host.lower():
        connection_type = "Session Pooler" if parsed.port == 5432 else "Transaction Pooler"

    return {
        "driver": parsed.drivername,
        "username": parsed.username,
        "host": host,
        "port": parsed.port,
        "database": parsed.database,
        "password_set": bool(parsed.password),
        "password_encoded_ok": "%" in (parsed.password or "") or True,
        "connection_type": connection_type,
        "masked_url": mask_database_url(url),
    }


def debug_database_config() -> dict:
    """
    Log and return diagnostic info about the database configuration.
    Password is never printed — only masked values.
    """
    raw = os.getenv("DATABASE_URL")
    sanitized = _sanitize_database_url(raw)

    print("\n--- Database Configuration Debug ---")

    if not raw:
        print("DATABASE_URL loaded: NO (missing from environment)")
        print(f".env path checked: {_ENV_PATH}")
        print("--- End Database Debug ---\n")
        raise ValueError("DATABASE_URL is not set in backend/.env")

    print("DATABASE_URL loaded: YES")
    print(f".env path: {_ENV_PATH}")

    if raw != sanitized:
        print("WARNING: DATABASE_URL value was sanitized (duplicate prefix or quotes removed)")
        print(f"  Raw (masked):    {mask_database_url(_sanitize_database_url(raw) or raw)}")
    else:
        print(f"  Masked URL:      {mask_database_url(sanitized)}")

    info = parse_database_url_info(sanitized)

    print("Parsed URL components:")
    print(f"  driver:          {info['driver']}")
    print(f"  username:        {info['username']}")
    print(f"  host:            {info['host']}")
    print(f"  port:            {info['port']}")
    print(f"  database:        {info['database']}")
    print(f"  password set:    {info['password_set']}")
    print(f"  connection type: {info['connection_type']}")

    if info["connection_type"] == "Direct Connection":
        print("  NOTE: Direct connections use IPv6-only hosts on some networks.")
        print("        If connection fails, switch to Session Pooler in Supabase dashboard.")

    print("--- End Database Debug ---\n")

    return info


def _require_database_url() -> str:
    url = _sanitize_database_url(DATABASE_URL) or _sanitize_database_url(os.getenv("DATABASE_URL"))

    if not url:
        raise ValueError(
            "DATABASE_URL is not set. Add it to backend/.env — "
            "e.g. postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
        )

    parse_database_url_info(url)
    return url


def init_engine() -> Engine:
    """Create the SQLAlchemy engine and session factory."""
    global engine, SessionLocal

    debug_database_config()
    url = _require_database_url()

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"sslmode": "require"},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SQLAlchemy engine created for host: %s", make_url(url).host)
    return engine


def create_tables() -> None:
    """
    Create all tables registered with Base.metadata.
    Models must be imported first so SQLAlchemy knows about them.
    """
    if engine is None:
        init_engine()

    assert engine is not None

    import models  # noqa: F401 — registers models with Base.metadata

    Base.metadata.create_all(bind=engine)
    _migrate_analysis_history_schema(engine)
    table_names = ", ".join(Base.metadata.tables.keys())
    print(f"Database tables created/verified: {table_names}")


def _migrate_analysis_history_schema(db_engine: Engine) -> None:
    """Apply lightweight schema updates for existing deployments."""
    from sqlalchemy import inspect

    inspector = inspect(db_engine)
    if "analysis_history" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("analysis_history")}
    if "created_at" in columns and "analyzed_at" not in columns:
        with db_engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE analysis_history RENAME COLUMN created_at TO analyzed_at")
            )
        print("Migrated analysis_history.created_at -> analyzed_at")

    columns = {col["name"] for col in inspector.get_columns("analysis_history")}
    if "project_type" not in columns:
        with db_engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE analysis_history "
                    "ADD COLUMN project_type VARCHAR(50) NOT NULL DEFAULT 'Web Application'"
                )
            )
        print("Migrated analysis_history: added project_type column")

    columns = {col["name"] for col in inspector.get_columns("analysis_history")}
    if "user_id" not in columns:
        with db_engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE analysis_history "
                    "ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE"
                )
            )
        print("Migrated analysis_history: added user_id column")


def verify_database_connection() -> None:
    """
    Test the database connection with a simple query.
    Raises on failure so callers can handle errors explicitly.
    """
    if engine is None:
        init_engine()

    assert engine is not None

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Connection test result: SUCCESS")
    except SQLAlchemyError as exc:
        print(f"Connection test result: FAILED — {exc}")
        raise ConnectionError(f"Unable to connect to PostgreSQL: {exc}") from exc


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""
    if SessionLocal is None:
        init_engine()

    assert SessionLocal is not None

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
