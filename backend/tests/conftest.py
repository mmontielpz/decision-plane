import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient


# Ensure backend root is importable
BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """
    Create a writable temporary database path for tests.
    """
    db_dir = tmp_path_factory.mktemp("db")
    return db_dir / "test_metadata.db"


@pytest.fixture(autouse=True)
def clean_state(monkeypatch, test_db_path):
    """
    Ensure a clean and deterministic state for each test.

    - Forces DATABASE_PATH to a temp SQLite file
    - Removes DB file before each test
    - Re-initializes schema
    """
    monkeypatch.setenv("DATABASE_PATH", str(test_db_path))

    if test_db_path.exists():
        test_db_path.unlink()

    from app.db.models import init_db
    init_db()

    yield


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)
