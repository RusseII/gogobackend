from validate_email import validate_email
while True:
	email = input()

	
	is_valid = validate_email(email,check_mx=True)
	print(is_valid)
	