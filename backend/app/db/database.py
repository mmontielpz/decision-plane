import os
import sqlite3
from pathlib import Path


def _resolve_database_path() -> Path:
    """
    Resolve the SQLite database path from environment variables.

    Priority:
    1. DATABASE_PATH env var
    2. Default: backend/data/db/metadata.db (canonical)

    Ensures the parent directory exists.
    """
    db_path_env = os.getenv("DATABASE_PATH")

    if db_path_env:
        db_path = Path(db_path_env).expanduser().resolve()
    else:
        repo_root = Path(__file__).resolve().parents[3]
        db_path = repo_root / "backend" / "data" / "db" / "metadata.db"

    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection with row factory enabled.
    Database path is resolved at call time to allow test isolation.
    """
    db_path = _resolve_database_path()
    print(">>> SQLITE CONNECT PATH:", db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn
