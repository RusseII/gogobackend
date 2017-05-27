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

        # set outgoing email from parsed resume
        destination_emails = email

        # parses first part of email (part before the @)
        # later used to personally great each user
        regex_str = r'^([^@]+)@[^@]+$'
        matchobj = re.search(regex_str, email)
        # group(1) is used to only select for the first part
        first_part_of_email = matchobj.group(1)

        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("Russsell@DeepHire.io")
        to_email = Email({email: "rwr21@zips.uakron.edu"})
        subject = "Happy Saturday!"
        content = Content("text/plain", "Hello " + first_part_of_email + "!")
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