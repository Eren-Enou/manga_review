from flask import Flask, render_template, request, Markup
# from flask_login import LoginManager

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi    
from datetime import datetime
from config import Config

import requests

app = Flask(__name__)
app.config.from_object(Config)

# Create a new client and connect to the server
client = MongoClient(Config.MONGODB_URI, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Create an instance of the LoginManager to set up Authentication
# login = LoginManager()
# login.init_app(app)
# Tell the login manager where to redirect if a user is not logged in
# login.login_view = 'login'
# login.login_message = "Hey you can't do that!"
# login.login_message_category = 'danger'

# from app import routes, models

# @login.user_loader
# def load_user(user_id):
#     return User.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)