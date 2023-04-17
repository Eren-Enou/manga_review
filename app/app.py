from flask import Flask, render_template, jsonify, request, Markup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi    
from datetime import datetime

import requests


app = Flask(__name__)

uri = "mongodb+srv://aarongblue:sLFIdkZsnq7I5HUZ@manga0.dsvoytg.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route('/reviews')
def reviews():
    # Get the user input from the request object
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    genre = request.args.get('genre', '')

    if (genre == ''):
        query = '''
        query ($page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            media (type: MANGA) {
            id
            title {
                romaji
                english
            }
            genres
            tags {
              name
            }
            averageScore
            description
            coverImage {
                large
            }
            }
        }
        }
        '''
    elif (genre != ''):
        query = '''
        query ($page: Int, $perPage: Int, $genre: String) {
        Page (page: $page, perPage: $perPage) {
            media (type: MANGA, genre: $genre) {
            id
            title {
                romaji
                english
            }
            genres
            tags {
              name
            }
            averageScore
            description
            coverImage {
                large
            }
            }
        }
        }
        '''

    # Define the query as a multi-line string
    

    # Define our query variables and values that will be used in the query request
    variables = {
        'page': int(page),
        'perPage': int(per_page),
        'genre': genre
    }

    url = "https://anilist-graphql.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": "87927f4031msh473a290f717da11p189432jsn9b635492ee37",
        "X-RapidAPI-Host": "anilist-graphql.p.rapidapi.com"
    }

    # Make the HTTP API request
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    # If the response status code is not 200, raise an exception
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))

    # Get the JSON response from the API
    data = response.json()

    # Extract media results from response
    media = data['data']['Page']['media']

    # Convert HTML strings to escaped Markup objects
    for m in media:
        m['description'] = Markup(m['description'])

    # Render reviews template with media data
    return render_template('reviews.html', media=media)



if __name__ == "__main__":
    app.run(debug=True)