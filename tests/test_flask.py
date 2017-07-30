# test_app.py
import pytest
from flask import url_for
import json
from bson import ObjectId
import sys
import time
import os
import http.client
sys.path.append('.')
from db.init import set_survey_questions, users, set_companies
from tests.test_sample import TestDbHandler


# uses test dv as specified in fixture


class TestFlask():

    def test_method(self, client):
        TestDbHandler().test_method()
        client_id = os.environ.get("AUTH0_ID")
        client_secret = os.environ.get("AUTH0_SECRET")
        conn = http.client.HTTPSConnection("deephire.auth0.com")
        payload = "{\"client_id\":\"" + client_id + "\",\"client_secret\":\"" + client_secret + "\",\"audience\":\"https://api.deephire.io\",\"grant_type\":\"client_credentials\"}"
        headers = {'content-type': "application/json"}
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        os.environ['AUTH0_TOKEN'] = data['access_token']

    def test_create_company(self, client):
        token = os.environ.get("AUTH0_TOKEN")

        headers = {'Content-Type': "application/json",
                   "authorization": 'Bearer ' + token}
        data = {
            "company": "dh3",
            "email": "russell@deephire.io",
            "user_id": 343433434
        }

        res = client.post(url_for('create_company'),
                          data=json.dumps(data), headers=headers)
        assert res.status_code == 201
        assert res.json['company_id']
        res = client.post(url_for('create_company'),
                          data=json.dumps(data), headers={"wrong": "d", "authorization": 'Bearer ' + token})
        assert res.status_code == 400
        res = client.post(url_for('create_company'),
                          data=json.dumps(data), headers={"authorization": 'Bearer ' + token})
        assert res.status_code == 400

        data = {
            "email": "russell@deephire.io",
            "user_id": 3434
        }
        res = client.post(url_for('create_company'),
                          data=json.dumps(data), headers=headers)
        assert res.status_code == 400

    def test_get_questions(self, client):
        token = os.environ.get("AUTH0_TOKEN")
        headers = {"authorization": 'Bearer ' + token}
        res = client.get(url_for('get_questions'), headers=headers)
        assert res.status_code == 200
        assert res.json
        assert res.json['questions']

    def test_get_comapnies(self, client):
        token = os.environ.get("AUTH0_TOKEN")
        headers = {"authorization": 'Bearer ' + token}
        res = client.get(
            url_for('get_companies', email="john@deephire.io"), headers=headers)
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(
            url_for('get_companies', email="russell@deephire.io"), headers=headers)
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(
            url_for('get_companies', email="test@lolwtf.com"), headers=headers)
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] is None

    def test_accounts_lookup_user_by_id(self, client):
        token = os.environ.get("AUTH0_TOKEN")
        headers = {"authorization": 'Bearer ' + token}
        res = client.get(url_for('accounts_lookup_user_by_id',
                                 user_id="596f6831202daf076567662a"), headers=headers)
        assert res.status_code == 200
        assert res.json
        assert res.json['company'] == "deephire"
        res = client.get(url_for('accounts_lookup_user_by_id',
                                 user_id="596c382dfd83e97fbc291130"), headers=headers)
        assert res.status_code == 204
        
        res = client.get(url_for('accounts_lookup_user_by_id',
                                 user_id="test@lolwtf.com"), headers=headers)
        assert res.status_code == 400

    def test_create_account(self, client):
        token = os.environ.get("AUTH0_TOKEN")
        headers = {'Content-Type': "application/json",
                   "authorization": 'Bearer ' + token}
        data = {
            "email": "russell@deephire.io"
        }
        res = client.post(url_for('create_account'),
                          data=json.dumps(data), headers=headers)

        assert res.status_code == 201
        assert res.json['user_id'] == "596f6831202daf076567662a"
        assert res.json['company'] == "deephire"

        data = {
            "email": "test_create_account@deephire.io"
        }
        res = client.post(url_for('create_account'),
                          data=json.dumps(data), headers=headers)
        assert res.status_code == 201
        assert res.json['company'] == "deephire"

    def test_submit_answers(self, client):
        token = os.environ.get("AUTH0_TOKEN")
        headers = {'Content-Type': "application/json",
                   "authorization": 'Bearer ' + token}
        data = {
            "user_id": "596f6831202daf076567662a",
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
