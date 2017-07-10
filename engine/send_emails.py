# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail, MailSettings, SandBoxMode


try:
    from engine.parse_files import ParseData
except:
    from parse_files import ParseData


class HandleEmail():

    def __init__(self):
        pass

    def send(self, email, unique_id=None, contents="No contents has been entered"):
        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))

        HtmlFile = open("engine/static/template.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        source_code = source_code.replace(
            "REPLACE", "https://www.deephire.io/login/" + unique_id)

        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        } # ,
                        # {"email": "rratcliffe57@gmail.com"
                        #  }
                    ],
                    "subject": "Thanks for making an account! Please confirm email."
                }
            ],
            "from": {
                "email": "Russell@DeepHire.io"
            },
            "content": [
                {
                    "type": "text/html",
                    "value": source_code
                }
            ]
        }
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def send_email_to_parsed(self, file):
        pd = ParseData()
        email = pd.find_emails(file)
        self.send(email)
        return ("email sent to " + email)


if __name__ == '__main__':
    print(HandleEmail().send("rwr21@zips.uakron.edu"))
