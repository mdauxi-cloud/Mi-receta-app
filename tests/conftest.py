import tempfile
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture
def app():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test.db"
        app = create_app({"TESTING": True, "DATABASE": str(db_path)})
        yield app


@pytest.fixture
def client(app):
    uploads_dir = Path(app.static_folder) / "uploads"
    before = set(uploads_dir.iterdir())
    yield app.test_client()
    for path in set(uploads_dir.iterdir()) - before:
        path.unlink()
