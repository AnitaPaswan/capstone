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
  dataDb=Movie.query.all()
  return render_template('pages/movies.html', areas=dataDb)


@app.route('/actors')
@requires_auth(permission='get:actors')
def actors(decoded_payload):
  actors = Actor.query.order_by(Actor.id).all()
  formatted_actors = [actor.short() for actor in actors]
  return jsonify(
    {"success": True,
     "actors" : formatted_actors
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "INTERNAL SERVER ERROR", "message": "Internal server error."}), 500



if __name__ == '__main__':
    app.run()