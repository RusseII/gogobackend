import pymongo
from bson import ObjectId
import os
import time
import random
# from db.init import set_survey_questions


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
            self.newsletter = self.client.deephire.newsletter

        if db == "test":
            self.questionnaires = self.client.test.questionnaires
            self.users = self.client.test.users
            self.orgs = self.client.test.orgs
            self.questions = self.client.test.questions
            self.responses = self.client.test.responses
            self.companies = self.client.test.companies
            self.newsletter = self.client.deephire.newsletter

    def initialize_questionnaire(self):

        self.questions.insert(set_survey_questions)

    def add_newslettter(self, email):
        # checks to see if someone with that email already registered
        exists = self.newsletter.find_one({"email": email})
        # if someone with that email already registered return True (so we can
        # make sure that we don't email that user again)
        if exists:
            return True
        self.newsletter.insert({"email": email})
        return False

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
        data.pop("user_id", None)
        for keys in data.keys():
            self.users.update(key, {"$set": {keys: data[keys]}}, True)
        # TODO fix this so it actually pics the correct survey
        # question instead of the first
        # inserts the survery questions grabbed before to the user profile

    def update_company(self, company_id, data):
        key = {"_id": ObjectId(company_id)}
        data.pop("company_id", None)
        for keys in data.keys():
            self.companies.update(key, {"$set": {keys: data[keys]}}, True)

    def update_company_calculate(self, company_id, data):
        key = {"_id": company_id}
        # data.pop("user_id", None)

        for x, question in enumerate(data['questions']):
            # print(question)
            response = question['response']
            print(self.companies.update(
                key, {"$set": {"questions." + str(x) + ".response": response}}))

    def lookup_user_by_id(self, user_id):
        user_data = self.users.find_one(ObjectId(user_id))
        return user_data

    def lookup_company_by_name(self, company_name):
        company_data = self.companies.find_one({"company": company_name})
        return company_data

    def get_id_from_email(self, email):
        data = self.users.find_one({"email": email})
        return data["_id"]

    def get_survey_questions(self, user_id=None, num=10):

        # this are in order with questions\
        if user_id == None:
            user = self.users.find_one({})
            user_id = str(user["_id"])
        x = 0
        question_content = []
        answered = False
        if num > 10:
            num = 10

        metrics = ["Recognition", "Ambassadorship", "Feedback", "Relationship with Peers",
                   "Relationship with Manager", "Satisfaction", "Alignment",
                   "Happiness", "Wellness", "Personal Growth"]
        user_info = self.users.find_one(ObjectId(user_id))
        for questions in user_info['questions']:

            if answered:
                answered = False
                if last_metric != questions['metric']:
                    x += 1
            if questions['response']:
                answered = True
                last_metric = questions['metric']
            else:
                if metrics[x] == questions['metric']:
                    x += 1
                    question_content.append(questions)
                    # this is to make sure that x is no incremented twice

            if x == 10:
                break

        if num != 10:
            indexs = random.sample(range(0, 10), num)
            print(indexs)

            shorter_questions = []
            for nums in indexs:
                shorter_questions.append(question_content[nums])
            question_content = shorter_questions

        # data = self.qquestions.find_one({})

        return {"questions": question_content}

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
        if self.companies.find_one({"company": company}):
            return "Company Exists"
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

    # def calculate_company_scores(self, company_id):
    #     company = self.companies.find_one(ObjectId(company_id))

    #     # 52 entires i think
    #     for x in range(52):
    #         total = 0
    #         num_of_peopple_answered = 0
    #         for user_ids in company['employees']:

    #             user_info = self.users.find_one(ObjectId(user_ids['user_id']))
    #             if user_info['questions'][x]['response']:
    #                 num_of_peopple_answered += 1
    #                 total += user_info['questions'][x]['response']
    #             # fix this up to account for people who didn;t answer
    #         if num_of_peopple_answered != 0:
    #             average_score = total / (num_of_peopple_answered)
    #         else:
    #             average_score = None

    #         company['questions'][x]['response'] = average_score
    #     self.companies.update_one(
    #         {"_id": ObjectId(company_id)}, {"$set": company})
       # update

    def calculate_company_scores2(self, company_id):
        company = self.companies.find_one(ObjectId(company_id))

        # 52 entires i think
        num_of_questions = len(company['questions'])

        for x in range(num_of_questions):
            total = 0
            num_of_peopple_answered = 0
            for user_ids in company['employees']:

                user_info = self.users.find_one(ObjectId(user_ids['user_id']))
                if user_info['questions'][x]['response']:
                    num_of_peopple_answered += 1
                    total += user_info['questions'][x]['response']
                # fix this up to account for people who didn;t answer
            if num_of_peopple_answered != 0:
                average_score = total / (num_of_peopple_answered)
            else:
                average_score = None

            company['questions'][x]['response'] = average_score

        self.update_company_calculate(ObjectId(company_id), company)
        # assert(False)
        # self.companies.update_one(
        #     {"_id": ObjectId(company_id)}, {"$set": company})
        return num_of_questions
       # update

    def get_company_domain_from_id(self, company_id):
        company = self.companies.find_one(ObjectId(company_id))
        return company['email_domain']

    def fill_company_info_with_fullcontact(self):
        pass


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

    handler = Db_Handler("test")
    print(handler.get_survey_questions("596f6831202daf076567662d", 2))

    # handler.register_user(user["email"], user)
    # x = '595aa8fefd83e97fbceac9e0'
    # # handler.initialize_questionnaire()
    # # print(handler.get_survey_questions())
    # # print(handler.lookup_user_by_id(x))
    # # print(handler.get_id_from_email("russell@deephire.io"))
    # # handler.questions.delete_many({})
    # # handler.questions.delete_many({})
    # # handler.users.delete_many({})
    # # handler.initialize_questionnaire()
    # data = {"email": "russell@deephire.io", "metric": "Recognition",
    #         "sub_metric": "Recognition Frequency",
    #         "text":
    #         "I am happy with how frequently I am recognized.", "response": 4}
    # print(handler.insert_answers(data))
