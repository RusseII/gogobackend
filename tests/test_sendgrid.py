import sendgrid
import os
from sendgrid.helpers.mail import (Email, Content, Mail, MailSettings,
                                   SandBoxMode)


def test_send_email():
    sg = sendgrid.SendGridAPIClient(
        apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("Russsell@DeepHire.io")
    to_email = Email("rwr21@zips.uakron.edu")
    subject = "Happy Saturday!"
    mail_settings = MailSettings()
    mail_settings.sandbox_mode = SandBoxMode(True)
    content = Content("text/plain", "Hello " + "test" + "!")
    mail = Mail(from_email, subject, to_email, content)
    mail.mail_settings = mail_settings
    response = sg.client.mail.send.post(request_body=mail.get())
    assert(response.status_code == 200)
