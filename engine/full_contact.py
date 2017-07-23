import os
import requests
import json
from db.db_handler import Db_Handler


class FullContact():

    def __init__(self, db):
        pass
        self.db = db

    def lookup_company_update(self, company_id):
        print(self.db)
        key = os.environ.get("your_key")
        company_email_domain = Db_Handler(
            self.db).get_company_domain_from_id(company_id)

        x = requests.get('https://api.fullcontact.com/v2/company/lookup.json?domain=' + company_email_domain,
                         headers={"X-FullContact-APIKey": (key)})
        Db_Handler(self.db).update_company(company_id, x.json())
        return (x.json())
        # return
