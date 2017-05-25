# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *
import re
import sys
# custom libs
from parse_files import ParseData

import time

class HandleEmail():
	def __init__(self):
		pass

	def send(self, email):

		#set outgoing email from parsed resume
		destination_email = email

		# parses first part of email (part before the @)
		# later used to personally great each user
		regex_str = r'^([^@]+)@[^@]+$'
		matchobj = re.search(regex_str, email)
		# group(1) is used to only select for the first part
		first_part_of_email = matchobj.group(1)


		sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
		from_email = Email("Russsell@DeepHire.io")
		to_email = Email(destination_email)
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
	start = time.time()

	for i in range(1):
  		HandleEmail().send_email_to_parsed(sys.argv[1])
  	  
	end = time.time()
	print(end - start)