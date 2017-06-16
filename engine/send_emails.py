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

    def send(self, email, contents="No contents has been entered"):

        # data = {
        #     "personalizations": [{
        #         "to": [{
        #             "email": "john@example.com"
        #         }],
        #         "subject": "Hello, World!"
        #     }],
        #     "from": {
        #         "email": "John Doe"
        #     },
        #     "content": {
        #         "type": "text",
        #         "value": "Hello, World!"
        #     },
        #     "mail_settings": {
        #         "sandbox_mode": {
        #             "enable": True
        #         }
        #     }
        # }

        # set outgoing email from parsed resume
        destination_email = email

        if contents != "No contents has been entered":

            submitter_email = contents["userInfo"]['email']
            submitter_org = contents["userInfo"]['org']
            submitter_position = contents["userInfo"]['positionTitle']
            submitter_manager = contents["userInfo"]['isManager']

            # creates a list answers that contains all of the answers
            answers = [answer[0]["response"]
                       for answer in contents["responses"]]

            # changes list to a string with huge spaces between the questions
            answers = "\n".join(answers)

            contents = "submitter_email = " + submitter_email + "\n" + \
                "submitter_org = " + submitter_org + "\n" + \
                "submitter_position = " + submitter_position + "\n" + \
                "submitter_manager = " + submitter_manager + "\n" + \
                answers

        sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("Notify@DeepHire.io")
        to_email = Email(destination_email)

        if submitter_email:
            subject = submitter_email
        else:
            subject = "Survery submitted (but no email attached)"

        mail_settings = MailSettings()

        content = Content("text/plain", contents)
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
