import sys
from pathlib import Path
import shutil
import pytest
from fastapi.testclient import TestClient

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app
from app.db.models import init_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_state():
    """
    Ensure a clean and deterministic state for each test run.
    This fixture:
    - Removes the SQLite database file
    - Removes raw storage directories
    - Re-initializes the database schema explicitly
    """

    # Remove SQLite database if it exists
    db_path = Path("db/metadata.db")
    if db_path.exists():
        db_path.unlink()

    # Remove raw storage directory if it exists
    raw_path = Path("data/raw")
    if raw_path.exists():
        shutil.rmtree(raw_path)

    # Explicitly initialize database schema
    init_db()

    yield
