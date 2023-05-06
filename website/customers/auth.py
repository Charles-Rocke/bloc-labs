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
	# incoming post request from recieving view
	if	request.method	==	"POST":
		# add email to your session
		session['users_email']	=	request.form.get("name_of_your_input_field_here")
		# redirect to user next route to send to api 
		return redirect(url_for('your.redirect_route_here'))
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
	# payload
	payload = {
		"domain" : rp_id, 
		"domain_name" : rp_name,
		"email" : session["email"]
	}
	# recieve bloc api response
	response = requests.get(url="https://bloc-api.bloclabs.repl.co/users/signup", params=payload).json()
	# turn response into a python dictionary 
	response_object = json.loads(response)
	# set registration challenge
	current_registration_challenge = response_object["challenge"]
	# decode registration challenge to expected challenge (the 3 ='s at the end are EXTREMELY IMPORTANT and NEED TO BE ADDED IN)
	current_registration_challenge = base64.urlsafe_b64decode(f"{current_registration_challenge}===")
	# return response to bloc js package, this is returning to '2. EDIT' if you cntl + f or command + f
	return response


#####################
# verify registration
@auth.route("/verify-registration-response",	methods=["POST"])
def	handler_verify_registration_response():
	# data from coming from blocJS, '3. EDIT'
	body	=	request.get_data()
	# your payload for the api
	payload = {
		"request" : body,
		"domain" : rp_id,
		"origin" : origin,
		"user" : session["email"],
	}
	# recieve response from post request
	response = requests.post(url="https://bloc-api.bloclabs.repl.co/users/verify_signup", params= payload).json()
	# if user is verified
	if response["verified"] == True:
		# creating a new user object from your database
		new_user	=	YourUserModel(email=session["email"])
		# add and commit your user to your database
		db.session.add(new_user)
		db.session.commit()
		# login your user to your application
		# those who manually built their sessions, login user at this part of your authentication flow
		login_user(new_user,	remember=True)
		# flask feature to show user that they successfully signed up
		flash('Account created!', category = 'success')\
		# return this response to '3. EDIT'
		return response
	# otherwise they won't be logged in
	else:
		return {"verified":False}
	

	
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
	# incoming post request from recieving view
	if request.method == 'POST':
		# add email to your session
		session['email'] = request.form.get("name_of_your_login_input_field_here")
		# redirect to user next route to send to api 
		return redirect(url_for('your.redirect_route_here'))
		
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
	# decode registration challenge to expected challenge (AGAIN the 3 ='s at the end are EXTREMELY IMPORTANT and NEED TO BE ADDED IN)
	current_authentication_challenge = base64.urlsafe_b64decode(f"{current_authentication_challenge}===")
	# return response to bloc js package, this is returning to '6. EDIT' if you cntl + f or command + f
	return response


#####################
# verify authentication
@auth.route("/verify-authentication-response",	methods=["POST"])
def	hander_verify_authentication_response():
	# data from coming from blocJS, '7. EDIT'
	body	=	request.get_data()
	# your payload for the api
	payload = {
		"request" : body,
		"domain" : rp_id,
		"origin" : origin,
		"user" : session["email"],
	}
	# recieve response from post request
	response = requests.post(url="https://bloc-api.bloclabs.repl.co/users/verify_login", params= payload).json()
	# if user is verified
	if response["verified"] == True:
		# get user from your database
		user = YourUserModel.query.filter_by(email=session['email']).first()
		# login your user to your application
		# those who manually built their sessions, login user at this part of your authentication flow
		login_user(user,	remember=True)
		# flask feature to show user that they successfully signed up
		flash('Successfully logged in', category = 'success')
		# return this response to '7. EDIT'
		return response
	# otherwise they won't be logged in
	else:
		return {"verified":False}


################
#
#	Logout
#
################
@auth.route("/logout",	methods=["GET","POST"])
def logout():
		logout_user()
		return redirect(url_for('views.home'))