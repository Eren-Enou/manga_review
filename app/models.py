import base64
import os
from random import randint
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mongoengine import Document, StringField, DateTimeField


class User(Document):
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    email = StringField(max_length=75, required=True, unique=True)
    username = StringField(max_length=75, required=True, unique=True)
    password = StringField(max_length=255, required=True)
    date_created = DateTimeField(default=datetime.utcnow)
    token = StringField(max_length=32, unique=True)
    token_expiration = DateTimeField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'date_created': self.date_created
        }

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'date_created': self.date_created,
        }
    
    def get_token(self, expires_in=300):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revoke_token(self):
        now = datetime.utcnow()
        self.token_expiration = now - timedelta(seconds=1)
        db.session.commit()


@login.user_loader
def get_a_user_by_id(user_id):
    return db.session.get(User, user_id)


def random_photo_url():
    return f"https://picsum.photos/500?random={randint(1,100)}"
