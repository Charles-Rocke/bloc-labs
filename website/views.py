from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

################
#
#	App	Views
#
################
#	Home
@views.route("/",	methods=["GET",	"POST"])
def	home():
	return	render_template("app/home.html", user = current_user)

#	Pricing
@views.route("/pricing",	methods=["GET",	"POST"])
def	pricing():
	return	render_template("app/pricing.html", user = current_user)


################
#
#	Profile	Views
#
################
#	Setup
@views.route("/settings",	methods=["GET",	"POST"])
@login_required
def	settings():
	
	return	render_template("app/dashboard/profile/settings.html", user = current_user)

################
#
#	App	Docs	Views
#
################
# signup
@views.route("/docs/signup",	methods=["GET",	"POST"])
@login_required
def	docs_signup():
	return	render_template("app/dashboard/docs/signup.html", user = current_user)

# login
@views.route("/docs/login",	methods=["GET",	"POST"])
@login_required
def	docs_login():
	return	render_template("app/dashboard/docs/login.html", user = current_user)


################
#
#	Other	Views
#
################
@views.route("/debug",	methods=["GET",	"POST"])
def	debugging():
	return	render_template("demo-site/debug.html", user = current_user)