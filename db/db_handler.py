import pymongo
import pprint
from bson import Binary, Code, ObjectId
from bson.json_util import dumps
import os


class Db_Handler():

    def __init__(self):
        # can also pass in url to db as a string
        passw = os.environ.get('MONGO_PASS')
        usrn = os.environ.get('MONGO_NAME')
        # can also pass in url to db as a string
        self.client = pymongo.MongoClient(
            "mongodb://" + usrn + ":" + passw + "@mongo-db-production-shard-00-00-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-01-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-02-tjcvk.mongodb.net:27017/ Mongo-DB-Production?ssl=true&replicaSet=Mongo-DB-Production-shard-0&authSource=admin")
        self.questionnaires = self.client.deephire.questionnaires

        self.users = self.client.deephire.users
        self.orgs = self.client.deephire.orgs
        self.questions = self.client.deephire.questions
        # new roos code

        self.responses = self.client.deephire.responses

    def initialize_questionnaire(self):

        placeholder = {
            "_id": "5964c728202daf0a637ab8b0",
            "questions": [
                {
                    "creator": "Deephire",
                    "metric": "Recognition",
                    "sub_metric": "Recognition Frequency",
                    "text": "I feel I need to be recognized for my work more frequently. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Recognition",
                    "sub_metric": "Recognition Frequency",
                    "text": "I am receiving an appopriate amount of recognition. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Recognition",
                    "sub_metric": "Recognition Quality",
                    "text": "Upper management highlights achievements in the organization. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Recognition",
                    "sub_metric": "Recognition Quality",
                    "text": "My direct manager celebrates accomplishments with my peers. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Ambassadorship",
                    "sub_metric": "Championing",
                    "text": "I would recommend my friends to join my workplace. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Ambassadorship",
                    "sub_metric": "Championing",
                    "text": "I would refer my peers to work at my organization. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Ambassadorship",
                    "sub_metric": "Pride",
                    "text": "I feel proud to tell my friends and family about where I work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Ambassadorship",
                    "sub_metric": "Pride",
                    "text": "I enjoy talking about my workplace to those not in the organization. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Feedback Quality",
                    "text": "After receiving feedback, I know exactly what I need to do in order to improve. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Feedback Quality",
                    "text": "Feedback I receive leaves me confused. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Suggestions for Organization",
                    "text": "I feel that my organization values my opinions and suggestions. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Suggestions for Organization",
                    "text": "When I voice my opinions and suggestions, I feel I make an impact. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Feedback Frequency",
                    "text": "I require more feedback to learn how to grow. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Feedback",
                    "sub_metric": "Feedback Frequency",
                    "text": "I am receiving an appropriate amount of feedback from my direct manager. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Collaboration between Peers",
                    "text": "I work very well with my peers. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Collaboration between Peers",
                    "text": "My peers and I finish tasks together in an efficient way.  "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Communication between Peers",
                    "text": "I feel cautious when communicating with my peers. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Communication between Peers",
                    "text": "I feel I can speak my mind honestly and openly with my peers. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Trust between Peers",
                    "text": "I respect the people I work with. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Peers",
                    "sub_metric": "Trust between Peers",
                    "text": "There is a mutual respect between me and those I work with. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Collaboration with Manager",
                    "text": "Working with my direct manager is frictionless. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Collaboration with Manager",
                    "text": "My direct manager and I collaborate well together. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Communication with Manager",
                    "text": "I know what to expect when I speak with my direct manager. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Communication with Manager",
                    "text": "My direct manager freely shares his thoughts with the team. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Trust with Manager",
                    "text": "I feel I can share my thoughts with my direct manager. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Relationship with Manager",
                    "sub_metric": "Trust with Manager",
                    "text": "I feel I have to 'hold back' when I speak with my direct manager. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Compensation",
                    "text": "For the amount I contribute to my organization, I feel appropriately compensated. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Compensation",
                    "text": "Taking into account my effort, skills, and experience - I am paid fairly. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Role within Organization",
                    "text": "My role and responsibilies are unclear to me. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Role within Organization",
                    "text": "I know exactly what is required of me at work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Workplace",
                    "text": "I look forward to spending time at my workplace. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Satisfaction",
                    "sub_metric": "Workplace",
                    "text": "I enjoy spending time at my workplace. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Values",
                    "text": "My organization chooses what to do carefully, based on our values. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Values",
                    "text": "Decisions are made with my organization's values in mind. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Vision & Mission",
                    "text": "I think my organization is able to achieve its mission. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Vision & Mission",
                    "text": "The roadmap on how to achieve the vision of my organization is clear to everyone. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Ethics & Social Responsibility",
                    "text": "Everyone in my organization is treated fairly. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Alignment",
                    "sub_metric": "Ethics & Social Responsibility",
                    "text": "My organization treats people from all backgrounds fairly. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Happiness",
                    "sub_metric": "Happiness at Work",
                    "text": "After a day of work, I feel as if I've contributed to my organization's mission. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Happiness",
                    "sub_metric": "Happiness at Work",
                    "text": "I feel fulfillment from the work I accomplish at my organization. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Happiness",
                    "sub_metric": "Work-Life Balance / MERGE",
                    "text": "I feel supported by my workplace if personal issues arise. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Happiness",
                    "sub_metric": "Work-Life Balance / MERGE",
                    "text": "I am confident my organization will support me when personal or family issues arise. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Wellness",
                    "sub_metric": "Personal Health",
                    "text": "My organization actively tries to promote employee health and wellness. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Wellness",
                    "sub_metric": "Personal Health",
                    "text": "My organization promotes resources/programs to encourage employee wellness. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Wellness",
                    "sub_metric": "Stress",
                    "text": "I feel stressed out when it comes to work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Wellness",
                    "sub_metric": "Stress",
                    "text": "I am too stressed out when it comes to my work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Autonomy",
                    "text": "I feel micromanaged when it comes to my work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Autonomy",
                    "text": "I need more independence when it comes to my work. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Purpose",
                    "text": "I feel that by working here, I contribute to a larger goal. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Purpose",
                    "text": "I feel that my work does not make a difference. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Mastery",
                    "text": "I can think of a handful of ways to grow within my organization. "
                },
                {
                    "creator": "Deephire",
                    "metric": "Personal Growth",
                    "sub_metric": "Mastery",
                    "text": "I have the opportunity to grow within my organization. "
                }
            ]
        }

        self.questions.insert(placeholder)

    def register_user(self, email, data):
        key = {"email": email}
        for keys in data.keys():
            self.users.update(key, {"$set": {keys: data[keys]}}, True)
        survey_questions = Db_Handler().questions.find_one()
            
        print(survey_questions)
        self.users.update(key, {"$set": {"questions": (survey_questions)}}, True)

    def lookup_user_by_id(self, user_id):
        user_data = Db_Handler().users.find_one(ObjectId(user_id))
        return user_data

    def get_id_from_email(self, email):
        data = Db_Handler().users.find_one({"email": email})
        return data["_id"]

    def get_survey_questions(self):
        data = Db_Handler().questions.find_one({})
        return data

    def get_company_from_email(self, email):
        data = Db_Handler().users.find_one({"email": email})
        print(data)
        if data:
            return data['company']
        else:
            return None

    def insert_answers(self, data):
        print(data)
        email = data['email']
        text = data['text']
        key = {"$and": [{"email": email}, {"questions.text": text}]}
        del data['email']
        data = Db_Handler().users.update(
            key, {'$set': {'questions.$.response': data['response']}})


if __name__ == "__main__":
    import datetime
    user = {
        "first": "Russell",
        "last": "Ratcliffe",
        "email": "russell@deephire.io",
        "org": "DeepHire",
        "time": datetime.datetime.now()

    }

    handler = Db_Handler()
    handler.register_user(user["email"], user)
    x = '595aa8fefd83e97fbceac9e0'
    # handler.initialize_questionnaire()
    # print(handler.get_survey_questions())
    # print(handler.lookup_user_by_id(x))
    # print(handler.get_id_from_email("russell@deephire.io"))
    # handler.questions.delete_many({})
    # handler.questions.delete_many({})
    #handler.users.delete_many({})
    # handler.initialize_questionnaire()
    data = {"email": "russell@deephire.io", "metric": "Recognition",
            "sub_metric": "Recognition Frequency",
            "text":
            "I am happy with how frequently I am recognized.", "response": 4}
    #print(handler.insert_answers(data))
