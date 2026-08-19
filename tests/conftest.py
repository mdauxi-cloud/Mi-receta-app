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
    return app.test_client()
