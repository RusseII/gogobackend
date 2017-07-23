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

    def send(self, email, company, user_id="error", contents="No contents has been entered"):
        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))

        try:
            HtmlFile = open("engine/static/template.html",
                            'r', encoding='utf-8')
        except:
            HtmlFile = open("static/template.html", 'r', encoding='utf-8')

        source_code = HtmlFile.read()

        source_code = source_code.replace(
            "REPLACE", "https://www.deephire.io/login/" + user_id)

        data = {
            "personalizations": [

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

        if type(email) == str:
            # mail_to is redundent because i was getting a weird error without it.
            mail_to = {
                "to": [
                    {
                        "email": "russell@deephire.io"
                    }
                ],
                "subject": "Thanks for making an account! Please confirm email."
            }
            mail_to['to'][0]['email'] = email
            data['personalizations'].append(mail_to)

        if type(email) == list:
            for address in email:
                mail_to = {
                    "to": [
                        {
                            "email": "russell@deephire.io"
                        }
                    ],
                    "subject": "Thanks for making an account! Please confirm email."
                }
                mail_to['to'][0]['email'] = address
                print(" ")

                data['personalizations'].append(mail_to)
                for items in (data['personalizations']):
                    print(items['to'])

        response = sg.client.mail.send.post(request_body=data)
        print(data)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def send_email_to_parsed(self, file):
        pd = ParseData()
        email = pd.find_emails(file)
        self.send(email)
        return ("email sent to " + email)


if __name__ == '__main__':
    print(HandleEmail().send(
        "rwr21@zips.uakron.edu"))
