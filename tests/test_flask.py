# test_app.py
import pytest
from flask import url_for


class TestFlask:

    def test_get_questions(self, client):
        res = client.get(url_for('get_questions'))
        assert res.status_code == 200
        assert res.json
        assert res.json['questions']

    def test_get_comapnies(self, client):
        res = client.get(url_for('companies', id="596c382dfd83e97fbcd911d0"))
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire.io"
