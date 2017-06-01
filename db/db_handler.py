import pymongo
import pprint


class Db_Handler():

    def __init__(self):
        self.client = pymongo.MongoClient()  # can also pass in url to db as a string
        self.questionnaires = self.client.deephire.questionnaires
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

        

    def get_questionnaire(self):
        default_survey = self.questionnaires.find_one()
        return default_survey 
    def insert_one_response(self, data):
        self.responses.insert_one(data)


# handler = Db_Handler()
# handler.initialize_questionnaire()
# handler.get_questionnaire()
