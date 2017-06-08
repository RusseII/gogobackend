import pymongo
import pprint
import os



class Db_Handler():

    def __init__(self):
        passw = os.environ.get('MONGO_PASS')
        usrn = os.environ.get('MONGO_USER')
        self.client = pymongo.MongoClient("mongodb://"+ usrn + ":" + passw + "@mongo-db-production-shard-00-00-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-01-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-02-tjcvk.mongodb.net:27017/ Mongo-DB-Production?ssl=true&replicaSet=Mongo-DB-Production-shard-0&authSource=admin")  # can also pass in url to db as a string
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

if __name__ == "__main__":
  handler = Db_Handler()
  handler.initialize_questionnaire()
  print(handler.get_questionnaire())
