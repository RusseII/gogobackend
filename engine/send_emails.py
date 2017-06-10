# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail, MailSettings, SandBoxMode
import re

try:
    from engine.parse_files import ParseData
except:
    from parse_files import ParseData


class HandleEmail():
    def __init__(self):
        pass

    def send(self, email):

        data = {
            "personalizations": [{
                "to": [{
                    "email": "john@example.com"
                }],
                "subject": "Hello, World!"
            }],
            "from": {
                "email": "John Doe"
            },
            "content": {
                "type": "text",
                "value": "Hello, World!"
            },
            "mail_settings": {
                "sandbox_mode": {
                    "enable": True
                }
            }
        }

        # set outgoing email from parsed resume
        destination_email = email

        # parses first part of email (part before the @)
        # later used to personally great each user
        # regex_str = r'^([^@]+)@[^@]+$'
        # matchobj = re.search(regex_str, email[0])
        # # group(1) is used to only select for the first part
        # first_part_of_email = matchobj.group(1)

        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("Notify@DeepHire.io")
        to_email = Email(destination_email)
        subject = "Happy Saturday!"

        mail_settings = MailSettings()

        content = Content("text/plain", "Someone submitted a survey!")
        mail = Mail(from_email, subject, to_email, content)
        mail.mail_settings = mail_settings
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        # print(response.body)
        # print(response.headers)

    def send_email_to_parsed(self, file):
        pd = ParseData()
        email = pd.find_emails(file)
        self.send(email)
        return ("email sent to " + email)


if __name__ == '__main__':
    print(HandleEmail().send(
        ["rwr21@zips.uakron.edu", "rratcliffe57@gmail.com"]))
