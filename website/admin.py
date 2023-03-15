from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User
from website.app import db
from website.apis.users import user
import json

admin = Blueprint('admin', __name__)

################
#
#	App	admin
#
################
#	Home
@admin.route("/",	methods=["GET",	"POST"])
def	home():
	# users = user.get_all_users()
	url = user.named_url_reverse()
	return	render_template("admin/home.html", user = current_user)