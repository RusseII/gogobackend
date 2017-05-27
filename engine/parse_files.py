import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import docx2txt
import re
import csv

# custom librarys


# timing stuff that can be removes
import time


class ParseData():
	def __init__(self):
		pass
		# print("Creating ParseData Object")

	def word_parser(self, file):
		text = docx2txt.process(file)
		return text

	# will most likely return multiple emails
	def csv_parser(self, file):
		f = open(file, 'r')
		reader = csv.reader(f)
		data = [row for row in reader]

		# used to change list of lists into one flat list
		data = [item for sublist in data for item in sublist]
		return data

	def pdf_parser(self, file_1):
		print(file_1)
		fp = open(file_1, 'rb')
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		# Create a PDF interpreter object.
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		# Process each page contained in the document.

		for page in PDFPage.get_pages(fp):
			interpreter.process_page(page)
			file_1 = retstr.getvalue()

		return file_1

	def parse_emails_to_string(self, file):
		if file.endswith(".pdf"):
			return self.pdf_parser(file)

		elif file.endswith(".docx"):
			return self.word_parser(file)

		elif file.endswith(".doc"):
			return self.word_parser(file)

		elif file.endswith(".csv"):
			return self.csv_parser(file)

		else:
			raise ValueError("""The file that was passed to "parse_emails_to_string
				did not have a correct file extention""")

	def find_emails(self, file):
		data = self.parse_emails_to_string(file)
		if type(data) == list:
			return data
		
		if type(data) == str:
			temp = re.findall(r'[\w\.-]+@[\w\.-]+', data)
			return temp

if __name__ == '__main__':
	print(ParseData().find_emails('../tests/resumes/julie.doc'))
