import sys
import pytest
from mock import Mock
sys.path.append('.')
from engine.parse_files import ParseData
from engine.send_emails import HandleEmail
from db.db_handler import Db_Handler
import pymongo
import pprint
from bson import Binary, Code, ObjectId
from bson.json_util import dumps
import os


class TestDbHandler():
    db = Db_Handler("test")

    def test_create_company(self):
        self.db.companies.delete_one({"company": "deephire_test"})
        company_id = self.db.create_company(
            "deephire_test", "russell_test@deephire.io", 545645)
        obj = self.db.companies.find_one({"_id": company_id})
        assert(obj["company"] == "deephire_test")

    russell = {
        "first": "Russell",
        "last": "Ratcliffe",
        "email": "russell@deephire.io",
        "company": "deephire"
    }

    nick = {
        "first": "Nick",
        "last": "Crawford",
        "email": "nick@deephire.io",
        "company": "DeepHire"
    }

    emerson = {
        "first": "emerson",
        "last": "cloud",
        "email": "emerson@amazon.com",
        "company": "DeepHire"
    }

    def test_register_user(self):
        self.db.register_user("russell@deephire.io")
        self.db.register_user("nick@deephire.io")
        self.db.register_user("emerson@amazon.")
        self.db.register_user("steve@youtube.com")
        self.db.register_user("junk")

    def test_lookup_user_by_id(self):
        # should return whole user object
        obj = self.db.lookup_user_by_id('596c382dfd83e97fbcd911d0')
        assert(obj['email'] == "russell@deephire.io")
        assert(self.db.lookup_user_by_id('596c382dfd83e97fbcd911dd') is None)

    def test_get_company_from_email(self):
        assert(self.db.get_company_from_email(
            "russell@deephire.io") == "deephire")
        assert(self.db.get_company_from_email("wtf@deephire.io") == "deephire")
        assert(self.db.get_company_from_email("john@newco.com") is None)

    def test_insert_answers(self):
        obj = (self.db.insert_answers("596c382dfd83e97fbcd911d0",
                                      "I feel I need to be recognized for my work more frequently. ", 8))
        assert(obj['updatedExisting'])

    def test_add_employee_to_company(self):
        self.db.add_employee_to_company(
            "deephire_test", {"user_id": 343424252525})

    def test_increment_company_employee_count(self):
        key = {"company": "deephire_test"}
        temp = self.db.companies.find_one(key)
        before_num = temp["number_of_employees"]
        self.db.increment_company_employee_count("deephire_test")
        temp = self.db.companies.find_one(key)
        after_num = temp["number_of_employees"]
        assert((before_num + 1) == after_num)

    def test_calculate_company_scores(self):
        pass

class TestParseData():
    pd = ParseData()

    def test_find_emails(self):
        assert (self.pd.find_emails('tests/resumes/julie.doc') == [
            "jha12@zips.uakron.edu"
        ])
        assert (self.pd.find_emails('tests/resumes/kyle.docx') == [
            "Kjv13@zips.uakron.edu"
        ])
        assert (self.pd.find_emails('tests/resumes/russell.pdf') == [
            "Rwr21@zips.uakron.edu"
        ])
        assert (self.pd.find_emails(
            'tests/resumes/emails_test_find_emails.csv') == [
                "rwr21@zips.uakron.edu", "rwr21@zips.uakron.edu"
        ])


class TestSendGrid():
    hd = HandleEmail()

    @pytest.fixture
    def mock_send_grid(self):
        return Mock(spec=HandleEmail)

    def test_mock(self, mock_send_grid):
        mock_send_grid.send("rwr21@zips.uakron.edu")

    # @mock.patch('engine.send_emails.')
    # def test_send_grid(self):


if __name__ == '__main__':
    TestDbHandler().test_insert_answers()
    # TestDbHandler().db.users.delete_many({})
