import sys
import pytest
from mock import Mock
sys.path.append(".")
from engine.parse_files import ParseData
from engine.send_emails import HandleEmail
from db.db_handler import Db_Handler
import pymongo
import pprint
from bson import Binary, Code, ObjectId
from bson.json_util import dumps
import os
from db.init import set_survey_questions, users, set_companies


class TestDbHandler():
    db = Db_Handler("test")

    def test_method(self):
        self.db.questions.delete_many({})
        self.db.users.delete_many({})
        self.db.companies.delete_many({})

        self.db.questions.insert_one(set_survey_questions)
        self.db.users.insert_many(users)
        self.db.companies.insert_many(set_companies)

        survey_questions = self.db.questions.find_one(
            ObjectId("5964c728202daf0a637ab8b0"))

        the_users = self.db.users.find()
        for user_ids in the_users:
            the_id = (user_ids["_id"])
            key = {"_id": the_id}

            # inserts the survery questions grabbed before to the user profile
            self.db.users.update(
                key, {"$set": {"questions": (survey_questions["questions"])}},
                True)

    def test_create_company(self):
        # self.db.companies.delete_one({"company": "deephire_test"})
        company_id = self.db.create_company(
            "test_create_company", "roos_test@test_company.io",
            "596f6831202daf076567662a")
        obj = self.db.companies.find_one({"_id": company_id})
        assert(obj["company"] == "test_create_company")

    def test_register_user(self):
        self.db.register_user("test1.io")
        obj = self.db.users.find_one({"email": "test1.io"})
        assert(obj["email"] == "test1.io")

    def test_lookup_user_by_id(self):
        # should return whole user object
        obj = self.db.lookup_user_by_id("596f6831202daf076567662a")
        assert(obj["email"] == "russell@deephire.io")
        assert(self.db.lookup_user_by_id("596c382dfd83e97fbcd911dd") is None)

    def test_get_company_from_email(self):
        assert(self.db.get_company_from_email(
            "russell@deephire.io") == "deephire")
        assert(self.db.get_company_from_email("wtf@deephire.io") == "deephire")
        assert(self.db.get_company_from_email("john@newco.com") is None)

    def test_insert_answers(self):
        obj = (self.db.insert_answers("596f6831202daf076567662a",
                                      "I feel I need to be recognized for my work more frequently. ", 8))
        assert(obj["updatedExisting"])

    def test_add_employee_to_company(self):
        self.db.add_employee_to_company(
            "deephire_test", {"user_id": 343424252525})

    def test_increment_company_employee_count(self):
        self.db.increment_company_employee_count("test_increment")
        temp = self.db.companies.find_one(ObjectId("596eea8e9b4d3900087c2d53"))
        employee_count = temp["number_of_employees"]
        assert((employee_count) == 2)

    def test_calculate_company_scores(self):
        self.db.calculate_company_scores2("596eea8e9b4d3900087c2d52")

    def test_lookup_company_by_name(self):
        company = self.db.lookup_company_by_name("deephire")
        assert company["company"] == "deephire"

    def test_get_questions(self):
        questions_no_number = {"questions": [{"response": None, "creator": "Deephire", "metric": "Recognition", "sub_metric": "Recognition Frequency", "text": "I feel I need to be recognized for my work more frequently. "}, {"response": None, "creator": "Deephire", "metric": "Ambassadorship", "sub_metric": "Championing", "text": "I would recommend my friends to join my workplace. "}, {"response": None, "creator": "Deephire", "metric": "Feedback", "sub_metric": "Feedback Quality", "text": "After receiving feedback, I know exactly what I need to do in order to improve. "}, {"response": None, "creator": "Deephire", "metric": "Relationship with Peers", "sub_metric": "Collaboration between Peers", "text": "I work very well with my peers. "}, {"response": None, "creator": "Deephire", "metric": "Relationship with Manager", "sub_metric": "Collaboration with Manager", "text": "Working with my direct manager is frictionless. "}, {
            "response": None, "creator": "Deephire", "metric": "Satisfaction", "sub_metric": "Compensation", "text": "For the amount I contribute to my organization, I feel appropriately compensated. "}, {"response": None, "creator": "Deephire", "metric": "Alignment", "sub_metric": "Values", "text": "My organization chooses what to do carefully, based on our values. "}, {"response": None, "creator": "Deephire", "metric": "Happiness", "sub_metric": "Happiness at Work", "text": "After a day of work, I feel as if I've contributed to my organization's mission. "}, {"response": None, "creator": "Deephire", "metric": "Wellness", "sub_metric": "Personal Health", "text": "My organization actively tries to promote employee health and wellness. "}, {"response": None, "creator": "Deephire", "metric": "Personal Growth", "sub_metric": "Autonomy", "text": "I feel micromanaged when it comes to my work. "}]}
        questions = self.db.get_survey_questions("596f6831202daf076567662d")
        assert(questions == questions_no_number)

    def teardown_method(self):
        pass


class TestParseData():
    pd = ParseData()

    def test_find_emails(self):
        assert (self.pd.find_emails("tests/resumes/julie.doc") == [
            "jha12@zips.uakron.edu"
        ])
        assert (self.pd.find_emails("tests/resumes/kyle.docx") == [
            "Kjv13@zips.uakron.edu"
        ])
        assert (self.pd.find_emails("tests/resumes/russell.pdf") == [
            "Rwr21@zips.uakron.edu"
        ])
        assert (self.pd.find_emails(
            "tests/resumes/emails_test_find_emails.csv") == [
                "rwr21@zips.uakron.edu", "rwr21@zips.uakron.edu"
        ])


class TestSendGrid():
    hd = HandleEmail()

    @pytest.fixture
    def mock_send_grid(self):
        return Mock(spec=HandleEmail)

    def test_mock(self, mock_send_grid):
        mock_send_grid.send("rwr21@zips.uakron.edu")

    # @mock.patch("engine.send_emails.")
    # def test_send_grid(self):


if __name__ == "__main__":
    TestDbHandler().test_insert_answers()
    # TestDbHandler().db.users.delete_many({})
