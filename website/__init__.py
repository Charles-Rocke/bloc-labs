import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import dotenv_values


# Load environment variables based on Docker Compose file
# if env is from compose testing


if os.getenv('DOCKER_COMPOSE_FILE') == 'docker-compose-test.yaml':
	load_dotenv('.env.dev')
	print("loaded test env")
# if env is from compose production
elif os.getenv('DOCKER_COMPOSE_FILE') == 'docker-compose-prod.yaml':
	load_dotenv('.env.prod')
	print("loaded prod env")
else:
	load_dotenv('.env')
	print("loaded .env")

config = dotenv_values(".env")
print(config)
db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
	app = Flask(__name__)

	app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
	app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
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