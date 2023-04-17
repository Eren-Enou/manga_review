import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-string'
    MONGODB_URI = "mongodb+srv://aarongblue:sLFIdkZsnq7I5HUZ@manga0.dsvoytg.mongodb.net/?retryWrites=true&w=majority"

