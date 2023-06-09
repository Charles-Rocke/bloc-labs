from typing import Optional, List
from dataclasses import dataclass, field
from webauthn.helpers.structs import AuthenticatorTransport
from . import db
from flask_login import UserMixin
from sqlalchemy.orm import backref
import uuid


def _str_uuid():
    return str(uuid.uuid4())


# Users
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    # users unique id
    uid = db.Column(db.String(40), default=_str_uuid, unique=True)
    # users email
    email = db.Column(db.String(150), unique=True)
    # users pricing plan
    pricing_plan = db.Column(db.String(10))
    # user api key
    api_key = db.Column(db.String(), unique=True)
