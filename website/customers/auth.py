from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, _str_uuid
from . import db
from flask_login import login_user, logout_user, current_user
#################################
import	json
import requests
import base64

# import	uuid
#################################

#################################
auth = Blueprint('auth', __name__)


################
#
#	Configuration & Other Settings
#
################

#	your	domain
rp_id	=	"yourdomain.com"
#	your origin	site (basically just adding https:// if you don't use a sub-domain)
origin	=	"https://yourdomain.com"
# your site name
rp_name	=	"your domain name"

#	A	simple	way	to	persist	challenges	until	response	verification (extra layer of security that is required to use the api)
current_registration_challenge	=	None
current_authentication_challenge	=	None


################
#
#	Registration
#
################
# email signup 
@auth.route("/signup",	methods=["GET",	"POST"])
def	signup_email():
	return	render_template("app/auth/signup_email.html", user = current_user)

	
#####################
#	signup view
@auth.route("/auth/signup",	methods=["GET",	"POST"])
def	signup():
	if	request.method	==	"POST":
		# generate uuid
		user_uid = _str_uuid()
		# add uuid to session
		session["user_uid"] = user_uid
		# check if uuid already exists
		user	=	User.query.filter_by(uid=session['user_uid']).first()
		# if user uid already exists, generate a new uid
		if user:
			while user:
				user_uid = _str_uuid()
				# add uuid to session
				session["user_uid"] = user_uid
				# check if uuid already exists
				user	=	User.query.filter_by(uid=session['user_uid']).first()
				print(f'Final uid: {session["user_id"]}')
				
		# add email to session
		session['email']	=	request.form.get("email")

		#	check if user email already exists
		user	=	User.query.filter_by(email=session['email']).first()
		if	user:
				flash('Email	already	exists',	category='error')
		elif	len(session['email'])	<	4:
				flash('Email	must	be	longer	than	3	characters.',	category	=	'error')
		return redirect(url_for('auth.signup'))
	
	return	render_template("app/auth/signup.html", user = current_user)


#####################
# generate registration options
@auth.route("/generate-registration-options",	methods=["GET"])
def	handler_generate_registration_options():
	global current_registration_challenge
	# print("IN	GENERATE	REG	OPTIONS")
	# global	current_registration_challenge
	

	
	# # new_user	=	User(uid=session["user_uid"], email=session["email"])
	# # session["new_user"] = new_user
	# # print(session["new_user"])
	# # print(type(session["new_user"]))
	# '''
 # 	options	=	generate_registration_options(
	# 	rp_id=rp_id,
	# 	rp_name=rp_name,
	# 	user_id=user.uid,
	# 	user_name=user.email,
	# 	exclude_credentials=[{
	# 			"id":	cred.id,
	# 			"transports":	cred.transports,
	# 			"type":	"public-key"
	# 	}	for	cred	in	user.credentials],
	# 	authenticator_selection=AuthenticatorSelectionCriteria(
	# 			user_verification=UserVerificationRequirement.REQUIRED),
	# 	supported_pub_key_algs=[
	# 			COSEAlgorithmIdentifier.ECDSA_SHA_256,
	# 			COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
	# 	],
	# )
	# '''
	# options	=	generate_registration_options(
	# 		rp_id=rp_id,
	# 		rp_name=rp_name,
	# 		user_id=session["user_uid"],
	# 		user_name=session["email"],
			
	# 		authenticator_selection=AuthenticatorSelectionCriteria(
	# 				user_verification=UserVerificationRequirement.REQUIRED),
	# 		supported_pub_key_algs=[
	# 				COSEAlgorithmIdentifier.ECDSA_SHA_256,
	# 				COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
	# 		],
	# )
	
	# current_registration_challenge	=	options.challenge
	# print(options.challenge)
	# print(options)
	# print()
	# print()
	# print(f'options_to_json(options): {options_to_json(options)}')
	# print(f'type options_to_json(options): {type(options_to_json(options))}')
	# return	options_to_json(options)
	

	# payload
	payload = {
		"domain" : rp_id, 
		"domain_name" : rp_name,
		"email" : session["email"]
	}
	# recieve bloc api response
	response = requests.get(url="https://bloc-api.bloclabs.repl.co/users/signup", params=payload).json()
	# json response to get registration challenge 
	response_object = json.loads(response)
	# set registration challenge
	current_registration_challenge = response_object["challenge"]
	# decode registration challenge to future expected challenge
	current_registration_challenge = base64.urlsafe_b64decode(f"{current_registration_challenge}===")
	# return response to bloc js package
	return response


#####################
# verify registration
@auth.route("/verify-registration-response",	methods=["POST"])
def	handler_verify_registration_response():
	# print("IN	VERIFY	REG	OPTIONS")
	# # global	current_registration_challenge

	# get body and send to api to be parsed and verified
	print(session["email"])
	print(type(session["email"]))
	body	=	request.get_data()
	print("BODY:	",	type(body))
	print("payload")
	payload = {
		"request" : body,
		"domain" : rp_id,
		"origin" : origin,
		"user" : session["email"],
	}
	print("response")
	# get response from post request and print it
	response = requests.post(url="https://bloc-api.bloclabs.repl.co/users/verify_signup", params= payload).json()
	print(response)
	# # print("BODY:	",body)
	# # Decode UTF-8 bytes to Unicode, and convert single quotes 
	# # to double quotes to make it valid JSON
	# my_json_str = body.decode('utf8').replace("'", '"')
	# print(my_json_str)
	# print('- ' * 20)
	
	# # Load the JSON to a Python list & dump it back out as formatted JSON
	# data = json.loads(my_json_str)
	# print(type(data))
	# s = json.dumps(data)
	# print(type(s))
	
	# credential = RegistrationCredential.parse_raw(body)
	# print(type(credential))
	# 	# check if device used any transports
	# 	# assign a potentially used transport
	# 	# user_transports = ''
	# 	print(current_registration_challenge)
	# 	verification	=	verify_registration_response(
	# 			credential=credential,
	# 			expected_challenge=current_registration_challenge,
	# 			expected_rp_id=rp_id,
	# 			expected_origin=origin,
	# 	)

	# 	print(current_registration_challenge)
		
	# 	if credential.transports:
	# 		print("credential:", credential.transports)
	# 		print("credential type:", type(credential.transports))
	# 		for transports in credential.transports:
	# 			print(transports)
	# 			print(type(transports))
	# 			print("transports value:", transports.value)
	# 			print("transports value type:", type(transports.value))
	# 		# assign the value of the transport to be assigned to the user
	# 		user_transport = transports.value
	# 		user_transport_type = transports
	# 		print("user transport: ", user_transport)
	# 		print("user transport type: ", user_transport)

			
	# 		# create new_user just like new_credential
	# 		#	log	current	user	in
	# 		print(f'current user email: {session["email"]}')
	"""If user is verified """
	if response["verified"] == True:
		print(response)
		new_user	=	User(email=session["email"])
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user,	remember=True)
		flash('Account created!', category = 'success')
		return response
	else:
		return {"verified":False}
	# 		print("current  user and id: ", current_user.email, current_user.id)
	# 		# add new credential to current user
	# 		new_credential	=	WebAuthnCredential(
	# 				user_id = current_user.id,
	# 				credential_id=verification.credential_id,
	# 				credential_public_key=verification.credential_public_key,
	# 				current_sign_count=verification.sign_count,
	# 				credential_transport = str(user_transport_type)
					
	# 		)
	# 		# add credential to database
	# 		db.session.add(new_credential)
	# 		db.session.commit()
			
	# 		print("if statement verified")
	# 		return	{"verified"	:	True}
	# 	else:
	# # 		#	log	current	user	in
	# 		print(f'current user email: {session["email"]}')
	# 		new_user	=	User(email=session["email"])
	# 		db.session.add(new_user)
	# 		db.session.commit()
	# 		login_user(new_user,	remember=True)
	# 		flash('Account created!', category = 'success')
	# 		print("current  user and id: ", current_user.email, current_user.id)
	# 		# add new credential to current user
	# 		new_credential	=	WebAuthnCredential(
	# 				user_id = current_user.id,
	# 				credential_id=verification.credential_id,
	# 				credential_public_key=verification.credential_public_key,
	# 				current_sign_count=verification.sign_count
					
	# 		)
	# 		# add credential to database
	# 		db.session.add(new_credential)
	# 		db.session.commit()
			
	# 		print("else statement verified")
	# 		return	{"verified"	:	True}
	

	
################
#
#	Authentication
#
################

#	login email	view
@auth.route("/login",	methods=["GET",	"POST"])
def	login_email():
	return	render_template("app/auth/login_email.html", user = current_user)


#	login	view
@auth.route("/auth/login",	methods=["GET",	"POST"])
def	login():
	if request.method == 'POST':
		# get the users uid using the email
		session['email'] = request.form.get('email')
		print(session['email'])
		user = User.query.filter_by(email=session['email']).first()
		if user:
			return redirect(url_for('auth.login'))
		else:
				flash('Email does not exist', category='error')
	return	render_template("app/auth/login.html",	user = current_user)


#####################
# generate authentication options
@auth.route("/generate-authentication-options",	methods=["GET","POST"])
def	handler_generate_authentication_options():
	print("IN	GENERATE	AUTH	OPTIONS")
	global	current_authentication_challenge
	
	
	# # get user from session email
	# print("ASSIGNING	USER")
	
	# user	=	User.query.filter_by(email=session['email']).first()
	# # who is user?
	# print(user.email)
	# # what is users username?
	
	
	# # get corrent user from session
	# #user = User.query.filter_by(email=session['email']).first()
	# # get the users
	# print(f"USER.CREDENTIALS:	{user.credentials}")
	# options	=	generate_authentication_options(
	# 		rp_id=rp_id,
	# 		# allow_credentials=[{
	# 		# 		"type":	"public-key",
	# 		# 		"id":	cred.credential_id,
	# 		# 		"transports":	cred.credential_transport
	# 		# }	for	cred	in	user.credentials],
	# 		user_verification=UserVerificationRequirement.REQUIRED,
	# )
	
	# current_authentication_challenge	=	options.challenge
	
	# return	options_to_json(options)
	# payload
	payload = {
		"domain" : rp_id, 
		"email" : session["email"]
	}
	# recieve bloc api response
	response = requests.get(url="https://bloc-api.bloclabs.repl.co/users/login", params=payload).json()
	# json response to get registration challenge 
	response_object = json.loads(response)
	# set registration challenge
	current_authentication_challenge = response_object["challenge"]
	# decode registration challenge to future expected challenge
	current_authentication_challenge = base64.urlsafe_b64decode(f"{current_authentication_challenge}===")
	# return response to bloc js package
	return response


#####################
# verify authentication
@auth.route("/verify-authentication-response",	methods=["POST"])
def	hander_verify_authentication_response():
	print("IN	verify	AUTH	OPTIONS")
	global	current_authentication_challenge
	

	body	=	request.get_data()
	
	payload = {
		"request" : body,
		"domain" : rp_id,
		"origin" : origin,
		"user" : session["email"],
	}
	print("response")
	# get response from post request and print it
	response = requests.post(url="https://bloc-api.bloclabs.repl.co/users/verify_login", params= payload).json()

	"""If user is verified """
	if response["verified"] == True:
		print(response)
		user = User.query.filter_by(email=session['email']).first()
		login_user(user,	remember=True)
		flash('Account created!', category = 'success')
		return response
	else:
		return {"verified":False}
	# try:
	# 		credential	=	AuthenticationCredential.parse_raw(body)

	# 		#	Find	the	user's	corresponding	public	key
			
	# 		user = User.query.filter_by(email=session['email']).first()
	# 		user_credential	=	None
	# 		for	cred	in	user.credentials:
	# 				if	cred.credential_id	==	credential.raw_id:
	# 						user_credential	=	cred

	# 		if	user_credential	is	None:
	# 				raise	Exception("Could	not	find	corresponding	public	key	in	DB")

	# 		#	Verify	the	assertion
	# 		verification	=	verify_authentication_response(
	# 				credential=credential,
	# 				expected_challenge=current_authentication_challenge,
	# 				expected_rp_id=rp_id,
	# 				expected_origin=origin,
	# 				credential_public_key=user_credential.credential_public_key,
	# 				credential_current_sign_count=user_credential.current_sign_count,
	# 				require_user_verification=True,
	# 		)
	# except	Exception	as	err:
	# 		return	{"verified":	False,	"msg":	str(err),	"status":	400}

	# #	Update	our	credential's	sign	count	to	what	the	authenticator	says	it	is	now
	# user_credential.current_sign_count = verification.new_sign_count
	# # log user in
	# login_user(user, remember=True)
	# return	{"verified":	True}


################
#
#	Logout
#
################
@auth.route("/logout",	methods=["GET","POST"])
def logout():
		logout_user()
		return redirect(url_for('views.home'))