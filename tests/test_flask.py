# test_app.py
import pytest
from flask import url_for
import json


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
        assert res.json['company'] is None

    def test_accounts_lookup_user_by_id(self, client):
        res = client.get(url_for('accounts_lookup_user_by_id',
                                 user_id="596c382dfd83e97fbcd911d0"))
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(
            url_for('accounts_lookup_user_by_id', user_id="596c382dfd83e97fbc291130"))
        assert res.status_code == 200
        assert res.json is None
        res = client.get(url_for('accounts_lookup_user_by_id',
                                 user_id="test@lolwtf.com"))
        assert res.status_code == 400

    def test_create_account(self, client):
        headers = {'Content-Type': "application/json"}
        data = {
            "first": "Russell",
            "last": "Ratcliffe",
            "email": "russell@deephire.io",
            "company": "deephire"
        }
        res = client.post(url_for('create_account'),
                          data=json.dumps(data), headers=headers)

        assert res.status_code == 201
        assert res.json['user_id'] == "596c382dfd83e97fbcd911d0"
        assert res.json['company'] == "deephire"

    def test_submit_answers(self, client):
        headers = {'Content-Type': "application/json"}
        data = {
            "user_id": "596c382dfd83e97fbcd911d0",
            "text": "I feel I need to be recognized for my work more frequently. ",
            "response": 8
        }
        res = client.put(url_for('submit_answers'),
                         data=json.dumps(data), headers=headers)
        assert res.status_code == 201

        data = {
            "user_id": "596c3dfd83e97fbcd911d0",
            "text": "I feel I need to be recognized for my work more frequently. ",
            "response": 8
        }
        res = client.put(url_for('submit_answers'),
                         data=json.dumps(data), headers=headers)
        assert res.status_code == 400

        data = {
            "user_id": "596c3823fd83e97fbcd911d0",
            "text": "I feel I need to be recognized for my work more frequently. ",
            "response": 8
        }
        res = client.put(url_for('submit_answers'),
                         data=json.dumps(data), headers=headers)
        assert res.status_code == 200


# TestFlask().test_submit_answers(request)