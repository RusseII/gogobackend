import pymongo
import pprint


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

    def get_questionnaire(self):
        default_survey = self.questionnaires.find({"creator": "DeepHire"})
        return default_survey

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
