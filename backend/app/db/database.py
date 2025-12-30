# app/db/database.py
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]   # /.../risk-aware-ml-system
DB_PATH = PROJECT_ROOT / "db" / "metadata.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn
