# test_app.py
import pytest
from flask import url_for


class TestApp:

    def test_get_questions(self, client):
        res = client.get(url_for('get_questions'))
        assert res.status_code == 200
        assert res.json

