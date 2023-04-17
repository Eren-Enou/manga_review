import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    uri = "mongodb+srv://aarongblue:sLFIdkZsnq7I5HUZ@manga0.dsvoytg.mongodb.net/?retryWrites=true&w=majority"

