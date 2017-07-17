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
        res = client.get(url_for('get_companies', email="john@deephire.io"))
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(url_for('get_companies', email="russell@deephire.io"))
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(url_for('get_companies', email="test@lolwtf.com"))
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == None
