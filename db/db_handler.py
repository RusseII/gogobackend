import pymongo
import pprint
from bson import Binary, Code
from bson.json_util import dumps


class Db_Handler():

    def __init__(self):
        # can also pass in url to db as a string
        self.client = pymongo.MongoClient()
        self.questionnaires = self.client.deephire.questionnaires
        self.questions = self.client.deephire.questions
        self.users = self.client.deephire.users
        self.orgs = self.client.deephire.orgs

        self.responses = self.client.deephire.responses

    def initialize_questionnaire(self):
        self.questions.insert({
            "_id":
            ObjectId("5931a9fb9c9870798ac4d4e3"),
            "creator":
            "Deephire",
            "text":
            "Do you know what is expected of you at work?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ecda"),
            "creator":
            "Deephire",
            "text":
            "Do you have the materials and equipment to do your work right?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ecdb"),
            "creator":
            "Deephire",
            "text":
            "In the last seven days, have you received recognition or praise for doing good work?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ecdc"),
            "creator":
            "Deephire",
            "text":
            "Does your supervisor, or someone at work, seem to care about you as a person?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ecdd"),
            "creator":
            "Deephire",
            "text":
            "Is there someone at work who encourages your development?"
        }, {
            "_id": ObjectId("5931ab77f25839ce7e73ecde"),
            "creator": "Deephire",
            "text": "At work, do your opinions seem to count?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ecdf"),
            "creator":
            "Deephire",
            "text":
            "Does the mission/purpose of your company make you feel your job is important?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ece0"),
            "creator":
            "Deephire",
            "text":
            "Are your associates (fellow employees) committed to doing quality work?"
        }, {
            "_id": ObjectId("5931ab77f25839ce7e73ece1"),
            "creator": "Deephire",
            "text": "Do you have a best friend at work?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ece2"),
            "creator":
            "Deephire",
            "text":
            "In the last six months, has someone at work talked to you about your progress?"
        }, {
            "_id":
            ObjectId("5931ab77f25839ce7e73ece3"),
            "creator":
            "Deephire",
            "text":
            "In the last year, have you had opportunities to learn and grow?"
        }, {
            "_id":
            ObjectId("5931abf3f25839ce7e73ece4"),
            "creator":
            "Deephire",
            "text":
            "At work, do you have the opportunity to do what you do best every day?"
        })

        self.questionnaires.insert([{
            "org":
            "DeepHire",
            "questions": [{
                "question_id": ObjectId("5931a9fb9c9870798ac4d4e3")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecda")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecdb")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecdc")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecdd")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecde")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ecdf")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ece0")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ece1")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ece2")
            }, {
                "question_id": ObjectId("5931ab77f25839ce7e73ece3")
            }, {
                "question_id": ObjectId("5931abf3f25839ce7e73ece4")
            }]
        }])
        # yapf: disable
        survey = {
         "questions":
             [
               {"text" : "question 1"},
               {"text" : "question 2"},
               {"text" : "question 3"},
               {"text" : "question 4"},
               {"text" : "question 5"},
               {"text" : "question 6"},
               {"text" : "question 7"},
               {"text" : "question 8"},
               {"text" : "question 9"},
               {"text" : "question 10"},
               {"text" : "question 12"}
             ],
          "name": "Culture Assessment Test"
         }
        # yapf: enable
        self.questionnaires.insert_one(survey)

    def get_placeholder_analysis(self, data):
        """This is placeholder analysis.
           Demonstrates ability to match on n conditions on one collection
        """

        response = self.responses.aggregate([{
            "$match": {
                "$and": [{
                    "responses": "i hate my bodsfsvss"
                }, {
                    "organization": "DeepHire"
                }]
            }
        }])
        return response

    def get_total_responses(self, data):
        return self.responses({org: data.org})

    def register_user(self, data):
        self.users.insert_one(data)

    def register_org(self, data):
        self.orgs.insert_one(data)

    def get_questionnaire(self, org):
        questions = self.questionnaires.aggregate([{
            "$match": {
                "org": org
            }
        }, {
            "$unwind": "$questions"
        }, {
            "$lookup": {
                "from": "questions",
                "localField": "questions.question_id",
                "foreignField": "_id",
                "as": "ldefault"
            }
        }])
        return questions

    def insert_question(self, data):
        self.questions.insert_one(data)

    def get_custom_questions(self, data):
        return self.questions.find({"creator": data.creator})

    def insert_one_response(self, data):
        self.responses.insert_one(data)


user = {
    "first": "Steven",
    "last": "Gates",
    "email": "steven@deephire.io",
    "organization": "DeepHire"
}

# handler = Db_Handler()
# handler.register_user(user)
# handler.initialize_questionnaire()
# handler.get_questionnaire()
