# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail
import re

try:
    from engine.parse_files import ParseData
except:
    from parse_files import ParseData


class HandleEmail():

    def __init__(self):
        pass

    def send(self, email):


        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("Russsell@DeepHire.io")
        to_email = Email("rwr21@zips.uakron.edu")
        to_email.add_to(Email("rratcliffe57@gmail.com"))
        subject = "Happy Saturday!"
        content = Content("text/plain", "Hello "  + "!")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

    def send_email_to_parsed(self, file):
        pd = ParseData()
        email = pd.find_emails(file)
        self.send(email)
        return ("email sent to " + email)

if __name__ == '__main__':
    print(HandleEmail().send(["rwr21@zips.uakron.edu", "rratcliffe57@gmail.com"]))