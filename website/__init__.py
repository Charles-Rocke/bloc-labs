import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .util import get_env_variables, get_testing_env_variables, update_testing_env_variables
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # get env variables
    env_vars = get_testing_env_variables()
    if env_vars["SERVER_NAME"] == "testing":
        app.config["DEBUG"] == True
    else:
        app.config["SECRET_KEY"] = env_vars["SECRET_KEY"]
        app.config["SQLALCHEMY_DATABASE_URI"] = env_vars["DATABASE_URL"]
        app.config["DEBUG"] == False
        app.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=1)
        

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    # login_manager.login_view = 'views.debugging'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
