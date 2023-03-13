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
	
		from .views import views
		from .auth import auth
		from .util import util

		app.register_blueprint(views,url_prefix='/')
		app.register_blueprint(auth,url_prefix='/')
		app.register_blueprint(util,url_prefix='/')

		from .models import Form, User, WebAuthnCredential

		#create_database(app)

		login_manager = LoginManager()
		login_manager.login_view = 'auth.login'
		#login_manager.login_view = 'views.debugging'
		login_manager.init_app(app)

		@login_manager.user_loader
		def load_user(id):
				return User.query.get(int(id))


		return app

# def create_database(app):
# 		if not path.exists('website/' + DB_NAME):
# 				db.create_all(app=app)
# 				print('Created Database')