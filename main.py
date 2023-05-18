from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
def create_app():
		app = Flask(__name__)
		app.config['SECRET_KEY'] = 'asdfghjkl'
		app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
		db.init_app(app)
		migrate.init_app(app, db)
	
		from website import views, auth, util

		app.register_blueprint(views,url_prefix='/')
		app.register_blueprint(auth,url_prefix='/')
		app.register_blueprint(util,url_prefix='/')

		from website.models import Form, User, Credential,	UserAccount, WebAuthnCredential

		#create_database(app)

		login_manager = LoginManager()
		login_manager.login_view = 'auth.login'
		#login_manager.login_view = 'views.debugging'
		login_manager.init_app(app)

		@login_manager.user_loader
		def load_user(id):
				return User.query.get(int(id))


		return app