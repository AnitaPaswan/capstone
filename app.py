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
from models import movie, Show, actor, db
from datetime import datetime,timedelta
from auth import AuthError, requires_auth
from flask_cors import CORS
from models import setup_db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


  @app.after_request

  def after_request(response):
     response.headers.add("Access-Control-Allow-Headers","ContentType, Authorization")
     response.headers.add("Access-Control-Allow-Methods", "GET, DELETE,POST, PATCH")
     return response
  
  @app.route('/')
  def index():
     return render_template('pages/home.html')
  
  @app.route('/movies')
  def movies():
    dataDb=movie.query.all()
    return render_template('pages/movies.html', areas=dataDb)
  
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
