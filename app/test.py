from flask import Flask, render_template, jsonify, request, Markup, redirect, url_for, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi    
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

import requests


app = Flask(__name__)

uri = "mongodb+srv://aarongblue:sLFIdkZsnq7I5HUZ@manga0.dsvoytg.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Manga0']
collection = db['users']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

from app import routes
from app import models

routes
models

if __name__ == "__main__":
    app.run(debug=True)