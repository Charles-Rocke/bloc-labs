import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
	app = Flask(__name__)
	# load in environment variables
	load_dotenv()
	app.config['SECRET_KEY'] = 'devenv' or os.getenv("PROD_SECRET_KEY")
	# Configure SQLite3 for development
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'

	# Configure PostgreSQL for production
	if os.getenv('ENV') == 'production':
		app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  
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