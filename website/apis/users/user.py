from flask import request, session, flash, url_for
from fastapi import FastAPI, Request
import uvicorn
import json

from	webauthn	import	(
		generate_registration_options,
		verify_registration_response,
		generate_authentication_options,
		verify_authentication_response,
		options_to_json,
)
from	webauthn.helpers.structs	import	(
		AuthenticatorSelectionCriteria,
		UserVerificationRequirement,
		RegistrationCredential,
		AuthenticationCredential,
)
from	webauthn.helpers.cose	import	COSEAlgorithmIdentifier

from website.app import db
from website.models import User, WebAuthnCredential, _str_uuid
from flask_login import login_user, login_required, logout_user, current_user

api = FastAPI(docs_url="/redoc_url")


### User api views

# GETS
# get all users
@api.get("/user")
def get_all_users():
	users = User.query.all()

	response_list = []
	for user in users:
		response_dict = {}
		response_dict["id"] = user.uid
		response_dict["email"] = user.email
		response_list.append(response_dict)
		
	json_formatted_str = json.dumps(response_list, indent=2)
	# response = json.dumps(response_list)
	return json_formatted_str
	
# get registration options from client
@api.get("/registration")
def register(rp_id: str, rp_name: str, user_id: str, username: str):
	global current_registration_challenge
	
	options	=	generate_registration_options(
			rp_id=rp_id,
			rp_name=rp_name,
			user_id=user_id,
			user_name=username,
			
			authenticator_selection=AuthenticatorSelectionCriteria(
					user_verification=UserVerificationRequirement.REQUIRED),
			supported_pub_key_algs=[
					COSEAlgorithmIdentifier.ECDSA_SHA_256,
					COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
			],
	)
	
	current_registration_challenge	=	options.challenge
	print("Hello")
	print(type(options))
	print("Wow")
	print(options)
	return options_to_json(options)


# verify registration from client
@api.post("/verify-reg")
def verify_reg(rp_id: str, origin: str):
	print("IN	VERIFY	REG	OPTIONS")
	global	current_registration_challenge
	

	body	=	request.get_data()
	print("BODY:	",	type(body))
	print("BODY:	",body)
	try:
		credential = RegistrationCredential.parse_raw(body)
		# check if device used any transports
		# assign a potentially used transport
		# user_transports = ''
		verification	=	verify_registration_response(
				credential=credential,
				expected_challenge=current_registration_challenge,
				expected_rp_id=rp_id,
				expected_origin=origin,
		)
		
		if credential.transports:
			print("credential:", credential.transports)
			print("credential type:", type(credential.transports))
			for transports in credential.transports:
				print(transports)
				print(type(transports))
				print("transports value:", transports.value)
				print("transports value type:", type(transports.value))
			# assign the value of the transport to be assigned to the user
			user_transport = transports.value
			user_transport_type = transports
			print("user transport: ", user_transport)
			print("user transport type: ", user_transport)

			
			# create new_user just like new_credential
			#	log	current	user	in
			print(f'current user email: {session["email"]}')
			new_user	=	User(email=session["email"])
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user,	remember=True)
			flash('Account created!', category = 'success')
			print("current  user and id: ", current_user.email, current_user.id)
			# add new credential to current user
			new_credential	=	WebAuthnCredential(
					user_id = current_user.id,
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count,
					credential_transport = str(user_transport_type)
					
			)
			# add credential to database
			db.session.add(new_credential)
			db.session.commit()
			
			print("if statement verified")
			return	{"verified"	:	True}
		else:
			#	log	current	user	in
			print(f'current user email: {session["email"]}')
			new_user	=	User(email=session["email"])
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user,	remember=True)
			flash('Account created!', category = 'success')
			print("current  user and id: ", current_user.email, current_user.id)
			# add new credential to current user
			new_credential	=	WebAuthnCredential(
					user_id = current_user.id,
					credential_id=verification.credential_id,
					credential_public_key=verification.credential_public_key,
					current_sign_count=verification.sign_count
					
			)
			# add credential to database
			db.session.add(new_credential)
			db.session.commit()
			
			print("else statement verified")
			return	{"verified"	:	True}
		
	except	Exception	as	err:
			return	{"verified":	False,	"msg":	str(err),	"status":	400}

