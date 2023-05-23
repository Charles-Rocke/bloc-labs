import os
from os import environ
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import requests
import json

# Helper methods
# get env variables from render
def get_env_variables():
	url = "https://api.render.com/v1/services/srv-chlpgp64dadfmshgctv0/env-vars?limit=20"

	headers = {
		"accept": "application/json",
		"authorization": "Bearer rnd_h2ezMpqcy92kIx4mNCanLdoCTP1e"
	}

	response = requests.get(url, headers=headers).json()
	return response


db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
	app = Flask(__name__)
	# get env variables
	env_vars = get_env_variables()
	print(env_vars)
	print(type(env_vars))
	app.config["SECRET_KEY"] = env_vars[0]["envVar"]["value"]
	app.config["SQLALCHEMY_DATABASE_URI"] = env_vars[1]["envVar"]["value"]
	
	db.init_app(app)
	migrate.init_app(app, db)

	from .views import views
	from .auth import auth
	from .util import util

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(util, url_prefix='/')

	from .models import Form, User, Credential, UserAccount, WebAuthnCredential

	# create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	# login_manager.login_view = 'views.debugging'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app