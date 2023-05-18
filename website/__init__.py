import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app(db_url = None):
	app = Flask(__name__)
	# load in environment variables
	load_dotenv()
	app.config['SECRET_KEY'] = 'asdfghjkl' or os.getenv("SECRET_KEY")
	# connection location string to data base and create a way to switch from devlopment and production
	app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
	db.init_app(app)
	migrate.init_app(app, db)

	from.views import views
	from.auth import auth
	from.util import util

	app.register_blueprint(views,url_prefix='/')
	app.register_blueprint(auth,url_prefix='/')
	app.register_blueprint(util,url_prefix='/')

	from .models import Form, User, Credential,	UserAccount, WebAuthnCredential

	#create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	#login_manager.login_view = 'views.debugging'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
			return User.query.get(int(id))


	return app