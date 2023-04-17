from app import db, collection, app

from flask import render_template, jsonify, request, Markup, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm, SearchForm
from app.models import User  
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

import requests

user_collection = db['users']


@app.context_processor
def inject_now():
    return {'current_year': datetime.utcnow().year}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Validated')
        flash('Form validated!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Check to see if there is already a user with either username or email    
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        new_user.add_to_db()
        document = collection.find_one({"first_name":first_name})
        if (document):
            flash(f"Thank you {document['first_name']} for signing up!", "success")
            print('Inserted document ID:', new_user.inserted_id)
            new_user.set_id(new_user.inserted_id)
        else:
            flash('Warning, failure','error')
            print("Warning, something didn't happen")
            print(document)
        return redirect(url_for('index'))
    else:
        print('warning, no validate')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        test = collection.find_one({"username":username})
        user = User(**test)
        if user is not None and user.check_password(password_guess=password):
            print(user.check_password(password_guess=password))
            login_user(user)
            flash(f"You have successfully logged in as {username}", 'success')
            return redirect(url_for('index'))
        else:
            flash('Failure','error')
            print(user)

    return render_template('login.html', form=form)

@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    db.users.insert_one(user)
    return jsonify({'result': 'success'})

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = db.users.find_one({'username': username})
    return jsonify(user)

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

