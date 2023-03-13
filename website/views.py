from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Form
from .app import db

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
#	Account	Views
#
################
#	Setup
@views.route("/account/setup",	methods=["GET",	"POST"])
@login_required
def	account_setup():
	
	return	render_template("app/account/setup.html", user = current_user)

################
#
#	App	Dash	Views
#
################
@views.route("/dashboard/home",	methods=["GET",	"POST"])
@login_required
def	dash_home():
	# save form
	if request.method == 'POST':
		header = request.form.get('header')
		field_name = request.form.get('field-name')
		primary_color = request.form.get('primary')
		secondary_color = request.form.get('secondary')
		company_name = request.form.get('company-name')
		
		new_form = Form(header=header, field_name=field_name, primary_color=primary_color, secondary_color=secondary_color, company_name=company_name, user_id=current_user.id)
		db.session.add(new_form)
		db.session.commit()
		
		for form in current_user.forms:
				print("company name: ", form)
			
		flash('Form created!', category='success')
		return	render_template("app/dashboard/home.html", user = current_user)
		
	return	render_template("app/dashboard/home.html", user = current_user)


################
#
#	Other	Views
#
################
@views.route("/debug",	methods=["GET",	"POST"])
def	debugging():
	return	render_template("demo-site/debug.html", user = current_user)