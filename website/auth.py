import os
from .util import get_env_variables, get_testing_env_variables
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, _str_uuid
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#################################
from typing import Dict
import json
import requests
import base64
import secrets
#################################
auth = Blueprint("auth", __name__)


################
#
# 	Server	Configuration & Other Settings
#
################
env_vars = get_testing_env_variables()
# mixpanel
from mixpanel import Mixpanel
mp = Mixpanel(env_vars["MIXPANEL_PROJECT_ID"])
# 	customers	domain
server_id = env_vars["SERVER_ID"]
# 	customer	origin	site
server_origin = env_vars["SERVER_ORIGIN"]
# origin	=	"https://bloc.id"
server_name = env_vars["SERVER_NAME"]

# 	A	simple	way	to	persist	challenges	until	response	verification
current_registration_challenge = None
current_authentication_challenge = None


################
#
# 	Registration
#
################
# email signup
@auth.route("/signup", methods=["GET", "POST"])
def signup_email():
    pricing_plan = ""
    # check for choice pricing plan
    if request.method("POST"):
        # if growth plan
        if request.form.get("growth"):
            pricing_plan = "growth"
            session["pricing_plan"] = pricing_plan
        # if enterprise
        elif request.form.get("enterprise"):
            pricing_plan = "enterprise"
            session["pricing_plan"] = pricing_plan
        # else is starter
        else:
            pricing_plan = "starter"
            session["pricing_plan"] = pricing_plan
    return render_template("app/auth/signup_email.html", user=current_user)


#####################
# 	signup view
@auth.route("/auth/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # generate uuid
        user_uid = _str_uuid()
        # add uuid to session
        session["user_uid"] = user_uid
        # check if uuid already exists
        user = User.query.filter_by(uid=session["user_uid"]).first()
        # if user uid already exists, generate a new uid
        if user:
            while user:
                user_uid = _str_uuid()
                # add uuid to session
                session["user_uid"] = user_uid
                # check if uuid already exists
                user = User.query.filter_by(uid=session["user_uid"]).first()
                print(f'Final uid: {session["user_id"]}')

        # add email to session
        session["email"] = request.form.get("email")

        # 	check if user email already exists
        user = User.query.filter_by(email=session["email"]).first()
        if user:
            flash("Email	already	exists", category="error")
        elif len(session["email"]) < 4:
            flash("Email	must	be	longer	than	3	characters.", category="error")
        return redirect(url_for("auth.signup"))

    return render_template("app/auth/signup.html", user=current_user)


#####################
# generate registration options
@auth.route("/generate-registration-options", methods=["GET"])
def handler_generate_registration_options():
    global current_registration_challenge

    # payload
    payload = {
        "server_id": server_id,
        "server_name": server_name,
        "email": session["email"],
    }
    # recieve bloc api response
    response = requests.get(
        url="https://bloc-api.bloclabs.repl.co/bloc/users/signup", params=payload
    ).json()
    # json response to get registration challenge
    response_object = json.loads(response)
    # set registration challenge
    current_registration_challenge = response_object["challenge"]
    # decode registration challenge to future expected challenge
    current_registration_challenge = base64.urlsafe_b64decode(
        f"{current_registration_challenge}==="
    )
    # return response to bloc js package
    return response


#####################
# verify registration
@auth.route("/verify-registration-response", methods=["POST"])
def handler_verify_registration_response():
    body = request.get_data()
    print("BODY:	", type(body))
    payload = {
        "request": body,
        "server_id": server_id,
        "server_origin": server_origin,
        "user": session["email"],
        "pricing_plan": session["pricing_plan"]
    }
    # get response from post request and print it
    response = requests.post(
        url="https://bloc-api.bloclabs.repl.co/bloc/users/verify_signup", params=payload
    ).json()

    if response["verified"] == True:
        print(response)
        new_user = User(email=session["email"])
        db.session.add(new_user)
        db.session.commit()
        # Note: you must supply the user_id who performed the event as the first parameter.
        login_user(new_user, remember=True)

        # tell mixpanel user is officially signed up
        mp.track(
            new_user.id,
            "Signed Up",
            {"Signup Type": "New User", "Username": new_user.email},
        )

        flash("Account created!", category="success")
        return response
    else:
        return {"verified": False}


################
#
# 	Authentication
#
################


# 	login email	view
@auth.route("/login", methods=["GET", "POST"])
def login_email():
    return render_template("app/auth/login_email.html", user=current_user)


# 	login	view
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get the users uid using the email
        session["email"] = request.form.get("email")
        print(session["email"])
        user = User.query.filter_by(email=session["email"]).first()
        if user:
            return redirect(url_for("auth.login"))
        else:
            flash("Email does not exist", category="error")
    return render_template("app/auth/login.html", user=current_user)


#####################
# generate authentication options
@auth.route("/generate-authentication-options", methods=["GET", "POST"])
def handler_generate_authentication_options():
    print("IN	GENERATE	AUTH	OPTIONS")
    global current_authentication_challenge

    payload = {"server_id": server_id, "email": session["email"]}
    # recieve bloc api response
    response = requests.get(
        url="https://bloc-api.bloclabs.repl.co/bloc/users/login", params=payload
    ).json()
    # json response to get registration challenge
    response_object = json.loads(response)
    # set registration challenge
    current_authentication_challenge = response_object["challenge"]
    # decode registration challenge to future expected challenge
    current_authentication_challenge = base64.urlsafe_b64decode(
        f"{current_authentication_challenge}==="
    )
    # return response to bloc js package
    return response


#####################
# verify authentication
@auth.route("/verify-authentication-response", methods=["POST"])
def hander_verify_authentication_response():
    print("IN	verify	AUTH	OPTIONS")
    global current_authentication_challenge

    body = request.get_data()

    payload = {
        "request": body,
        "server_id": server_id,
        "server_origin": server_origin,
        "user": session["email"],
    }
    print("response")
    # get response from post request and print it
    response = requests.post(
        url="https://bloc-api.bloclabs.repl.co/bloc/users/verify_login", params=payload
    ).json()

    """If user is verified """
    if response["verified"] == True:
        print(response)
        user = User.query.filter_by(email=session["email"]).first()
        login_user(user, remember=True)
        # tell mixpanel user is officially signed up
        mp.track(
            user.id,
            "Logged in",
            {"Login Type": "Existing User", "Username": user.email},
        )
        flash("Login successful!", category="success")
        return response
    else:
        return {"verified": False}


################
#
# 	Logout
#
################
@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("views.home"))
