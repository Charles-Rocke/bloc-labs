from flask import Blueprint, request, session
from flask_login import login_required, current_user
from .models import User, Form
from . import db

util = Blueprint('util', __name__)

################
#
#	Utilities
#
################
#	display form
@util.route("/form",	methods=["GET","POST"])
@login_required
def	display_form():
		if	request.method	==	'POST':
			# create an object for return
			form = {}
			# get current users form data
			user	=	User.query.filter_by(id=current_user.id).first()
			# loop through list to get form
			
			for forms in user.forms:
				form['header'] = forms.header
				form['fieldName'] = forms.field_name
				form['primaryColor'] = forms.primary_color
				form['secondaryColor'] = forms.secondary_color
				form['companyName'] = forms.company_name

			
			# return True for 'authenticated'
			return form
		# return False for 'not authenticated'
		else:
			return	{"form": False}