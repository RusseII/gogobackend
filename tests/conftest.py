# conftest.py
import sys
sys.path.append('.')
import pytest

from main import create_app


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app