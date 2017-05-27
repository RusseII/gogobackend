import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import docx2txt
import re

# timing stuff that can be removes
import time


class ParseData():
	def __init__(self):
		pass
		# print("Creating ParseData Object")

	def word_parser(self, file):
		text = docx2txt.process(file)
		return text

	def pdf_parser(self, file):

		fp = file(file, 'rb')
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
			file =  retstr.getvalue()

		return file

	def find_emails(self, file):
		data = self.parse_emails_to_string(file)
		temp = re.search(r'[\w\.-]+@[\w\.-]+', data)
		return temp.group()


	def parse_emails_to_string(self, file):
		if file.endswith(".pdf"):
			return self.pdf_parser(file)

		elif file.endswith(".docx"):
			return self.word_parser(file)

		elif file.endswith(".doc"):
			return self.word_parser(file)

		else:
			raise ValueError("""The file that was passed to "parse_emails_to_string
				did not have a correct file extention""")


	
if __name__ == '__main__':
	start = time.time()

	for i in range(1):
  	  print ParseData().find_emails(sys.argv[1])
  	  
	end = time.time()
	#print(end - start)

