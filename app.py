#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import Movie, Actor, db
from datetime import datetime,timedelta
from auth import AuthError, requires_auth
from flask_cors import CORS
from models import setup_db

app = Flask(__name__)
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)
setup_db(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers","ContentType")
    response.headers.add("Access-Control-Allow-Methods", "GET, DELETE,POST, PATCH")
    response.headers['Authorization'] = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1BWW5fdF80X0NXOXkzM09sWFlpOSJ9.eyJpc3MiOiJodHRwczovL2ZzZG4xMjMuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1MjQzY2ZhZTUwMTY0NDM1NGMyN2UyMyIsImF1ZCI6ImNhcDIiLCJpYXQiOjE2OTY5NTc4OTUsImV4cCI6MTY5NzA0NDI5NCwiYXpwIjoidzlXY1ptVkx4OHZuQTZDblc5cHRRNmxhUGk5NW01MVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6aG9tZSIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBvc3Q6YWN0b3IiXX0.UDgeKuFudkbjO1xTIotMoleNhwEUWu7txvK5n1vbpBzwyfhE1YMPjZHio1I9i2AZNpxtgYY6dUZjQcL99B16GmcHKy2NeLAontpU_c9wrb4OpcvK075WjyB-7LxoK1V95zcrMy6FD_gU4Ibx1goieP48vnTlWhKaMJI97_cGkBnthvw14zunmFEolYT3r4FsUSZOJYm2_SmPQNGDcsjBn21DqEDEzkEDfkBDr6Hq2nf5lsGnjswYtFpy9uhaialO_ac2sQ70LHyJrZ5iUc7f21j4fUO1pDTykAy3uY1f67Wls6vWA1AHb_AOC3dgpRBya7I8tYANZ65tkyBc2OZJVA'
    return response

@app.route('/')
def login():
  return render_template('pages/login.html')

@app.route('/home')
def index():
  return render_template('pages/home.html')

@app.route('/callback')
def callback():
    return redirect(url_for('index'))

@app.route('/movies')
@requires_auth(permission='get:movies')
def movies(decoded_payload):
  movies=Movie.query.order_by(Movie.id).all()
  if not movies:
        abort(404) 
  formatted_movies = [movie.short() for movie in movies]
  return jsonify(
    {"success": True,
     "movies" : formatted_movies
    })

@app.route('/movie', methods = ['POST'])
@requires_auth(permission='post:movie')
def create_movies(decoded_payload):
    body=request.get_json()
    new_title = body.get('title')
    new_release_date = body.get('release_date')
    try:
        movie = Movie(title=new_title, recipe=new_release_date)
        if new_title is None:
            return jsonify({"error": "New title not provided"}), 400
        if new_release_date is None:
            return jsonify({"error": "New release_date not provided"}), 400
        movie.insert()
        return jsonify({
            "success": True,
            "movies":Movie.query.order_by(Movie.id).all()
        })
    except: 
        abort(422)


@app.route('/actors')
@requires_auth(permission='get:actors')
def actors(decoded_payload):
  actors = Actor.query.order_by(Actor.id).all()
  if not actors:
        abort(404)
  formatted_actors = [actor.short() for actor in actors]
  return jsonify(
    {"success": True,
     "actors" : formatted_actors
    })

@app.route('/actor', methods = ['POST'])
@requires_auth(permission='post:actor')
def create_actors(decoded_payload):
    body=request.get_json()
    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')
    new_movie_id = body.get('movie_id')
    try:
        actor = Actor(name=new_name, age=new_age, gender=new_gender, movie_id=new_movie_id)
        movies_id_validation = Movie.query.order_by(Movie.id).all()
        if not movies_id_validation:
            abort(400, description="No movies found, Validate the movie id")
        if new_name is None:
            return jsonify({"error": "New title not provided"}), 400
        if new_age is None:
            return jsonify({"error": "New recipe not provided"}), 400
        if new_gender is None:
            return jsonify({"error": "New gender not provided"}), 400
        if new_age is None:
            return jsonify({"error": "New recipe not provided"}), 400
        actor.insert()
        return jsonify({
            "success": True,
            "drinks":Actor.query.order_by(Actor.id).all()
        })
    except: 
        abort(422)

@app.route('/actor', methods = ['PATCH'])
@requires_auth(permission='patch:actor')
def create_actors(decoded_payload):
    body=request.get_json()
    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')
    new_movie_id = body.get('movie_id')
    try:
        actor = Actor(name=new_name, age=new_age, gender=new_gender, movie_id=new_movie_id)
        movies_id_validation = Movie.query.order_by(Movie.id).all()
        if not movies_id_validation:
            abort(400, description="No movies found, Validate the movie id")
        if new_name is None:
            return jsonify({"error": "New title not provided"}), 400
        if new_age is None:
            return jsonify({"error": "New recipe not provided"}), 400
        if new_gender is None:
            return jsonify({"error": "New gender not provided"}), 400
        if new_age is None:
            return jsonify({"error": "New recipe not provided"}), 400
        actor.insert()
        return jsonify({
            "success": True,
            "drinks":Actor.query.order_by(Actor.id).all()
        })
    except: 
        abort(422)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": "Provided request body is not correct"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "INTERNAL SERVER ERROR", "message": "Internal server error."}), 500

@app.errorhandler(AuthError)
def handled_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response



if __name__ == '__main__':
    app.run()