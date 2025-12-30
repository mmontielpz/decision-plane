import sys
from pathlib import Path
import shutil
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is importable
BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app
from app.db.models import init_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_state():
    """
    Ensure a clean and deterministic state for each test.

    - Removes the SQLite database file used by backend
    - Removes raw storage directory
    - Re-initializes database schema
    """

    # Correct paths AFTER backend refactor
    db_path = BACKEND_ROOT / "db" / "metadata.db"
    raw_path = BACKEND_ROOT / "data" / "raw"

    if db_path.exists():
        db_path.unlink()

    if raw_path.exists():
        shutil.rmtree(raw_path)

    init_db()
    yield
