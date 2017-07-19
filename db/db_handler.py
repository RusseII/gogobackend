import pymongo
from bson import ObjectId
import os
  
from db.init import set_survey_questions


class Db_Handler():

    def __init__(self, db):
        # can also pass in url to db as a string
        passw = os.environ.get('MONGO_PASS')
        usrn = os.environ.get('MONGO_NAME')
        # can also pass in url to db as a string
        self.client = pymongo.MongoClient(
            "mongodb://" + usrn + ":" + passw + """@mongo-db-production-shard-00-00-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-01-tjcvk.mongodb.net:27017,mongo-db-production-shard-00-02-tjcvk.mongodb.net:27017/ Mongo-DB-Production?ssl=true&replicaSet=Mongo-DB-Production-shard-0&authSource=admin""")

        if db == "prod":
            self.questionnaires = self.client.deephire.questionnaires
            self.users = self.client.deephire.users
            self.orgs = self.client.deephire.orgs
            self.questions = self.client.deephire.questions
            self.responses = self.client.deephire.responses
            self.companies = self.client.deephire.companies

        if db == "test":
            self.questionnaires = self.client.test.questionnaires
            self.users = self.client.test.users
            self.orgs = self.client.test.orgs
            self.questions = self.client.test.questions
            self.responses = self.client.test.responses
            self.companies = self.client.test.companies

    def initialize_questionnaire(self):

        self.questions.insert(set_survey_questions)

    def register_user(self, email):
        key = {"email": email}
        if self.users.find_one(key) is not None:
            return "user already exists"
        else:
            self.users.insert_one(key, key)

        # TODO fix this so it actually pics the correct survey
        # question instead of the first
            survey_questions = self.questions.find_one()
            # inserts the survery questions grabbed before to the user profile
            self.users.update(
                key, {"$set": {"questions": (survey_questions['questions'])}},
                True)

    def update_user(self, user_id, data):
        key = {"_id": user_id}
        for keys in data.keys():
            self.users.update(key, {"$set": {keys: data[keys]}}, True)
        # TODO fix this so it actually pics the correct survey
        # question instead of the first
        # inserts the survery questions grabbed before to the user profile

    def lookup_user_by_id(self, user_id):
        user_data = self.users.find_one(ObjectId(user_id))
        return user_data

    def get_id_from_email(self, email):
        data = self.users.find_one({"email": email})
        return data["_id"]

    def get_survey_questions(self):
        # TODO this should be selecting by specific ID
        data = self.questions.find_one({})
        return data

    def get_company_from_email(self, email):
        # finds email domain to search
        email_domain = email.split("@")[1]

        data = self.users.find_one(
            {"email": {"$regex": ".*" + email_domain + ".*"}})

        if data:
            if 'company' in data:
                return data['company']
            else:
                return None
        else:
            return None

    def insert_answers(self, user_id, text, response):
        # data must have an email + text + response field
        key = {"$and": [{"_id": ObjectId(user_id)}, {"questions.text": text}]}
        data = self.users.update(
            key, {'$set': {'questions.$.response': response}})

        return data

    def create_company(self, company, email, user_id):
        creator = email
        email_domain = email.split("@")[1]
        company_info = {
            "company": company,
            "creator": creator, "email_domain": email_domain,
            "number_of_employees": 1,
            "employees": [{"user_id": user_id}]
        }
        company_id = self.companies.insert(company_info)
        survey_questions = self.questions.find_one()
        key = {"_id": company_id}
        self.companies.update(
            key, {"$set": {"questions": (survey_questions['questions'])}},
            True)
        return company_id

    def add_employee_to_company(self, company, user_id):
        key = {"company": company}
        self.companies.update_one(key, {"$push": {'employees': user_id}})
        self.increment_company_employee_count(company)
        return company

    def increment_company_employee_count(self, company):
        key = {"company": company}
        self.companies.update_one(key, {"$inc": {"number_of_employees": 1}})

    def calculate_company_scores(self, company_id):
        key = {"_id": company_id}
        company = self.companies.find(key)

        # 52 entires i think
        for x in range(50):
            total = 0
            for user_ids in company['employees']:
                key = {"_id": user_ids}
                user_info = self.employees.find_one(key)
                if user_info['questions'][x]['response']:
                    total += user_info['questions'][x]['response']
                # fix this up to account for people who didn;t answer
            average_score = total / (company['number_of_employees'])
            company['questions'][x]['response'] = average_score
        self.companies.update_one(key, company)
       # update


# def update_tags(ref, new_tag):
    # coll.update({'ref': ref}, {'$push': {'tags': new_tag}})

if __name__ == "__main__":
    import datetime
    user = {
        "first": "Russell",
        "last": "Ratcliffe",
        "email": "russell@deephire.io",
        "company": "DeepHire",
        "time": datetime.datetime.now()

    }

    handler = Db_Handler("prod")
    #handler.register_user(user["email"], user)
    x = '595aa8fefd83e97fbceac9e0'
    #handler.initialize_questionnaire()
    # print(handler.get_survey_questions())
    # print(handler.lookup_user_by_id(x))
    # print(handler.get_id_from_email("russell@deephire.io"))
    # handler.questions.delete_many({})
    # handler.questions.delete_many({})
    # handler.users.delete_many({})
    # handler.initialize_questionnaire()
    data = {"email": "russell@deephire.io", "metric": "Recognition",
            "sub_metric": "Recognition Frequency",
            "text":
            "I am happy with how frequently I am recognized.", "response": 4}
    # print(handler.insert_answers(data))
