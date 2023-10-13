#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import Actor, db, Movie
from datetime import datetime,timedelta
from auth import AuthError, requires_auth
from flask_cors import CORS, cross_origin
from models import setup_db
from urllib.parse import quote_plus, urlencode
import os

from authlib.integrations.flask_client import OAuth

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET =  os.environ['CLIENT_SECRET']

app = Flask(__name__)
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)
setup_db(app)
CORS(app)

oauth = OAuth(app)
oauth.register(
    name="auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    authorize_url="https://your-auth0-domain/authorize",
    authorize_params=None,
    authorize_params_callback=None,
    authorize_prompt_callback=None,
    authorize_response=None,
    fetch_token="https://your-auth0-domain/oauth/token",
    client_cls=None,
)
###############################
@app.route("/login")
def index():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/auth_login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    return render_template("pages/welcome.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

###################################


@app.route('/auth_login')
def auth_login():
  return render_template('pages/login.html')



# @app.route('/login')
# @cross_origin(headers = ["Content-Type", "Authorization"])
# def login():
#   return oauth.auth0.authorize_redirect(redirect_uri=url_for("start_login", _external=True))

# @app.route('/home')
# @cross_origin(headers = ["Content-Type", "Authorization"])
# def index():
#   access_token = urllib.parse.unquote(request.args.get('access_token'))
#   print(access_token)
#   full_url = request.url
#   print(full_url, "**********full_url*************")
#   return render_template('pages/home.html')

# @app.route('/callback')
# @cross_origin(headers = ["Content-Type", "Authorization"])
# def callback():
#   token = oauth.auth0.authorize_access_token()
#   session["user"] = token
#   return redirect(url_for('index'))

# @app.route("/callback", methods=["GET", "POST"])
# def callback():
#     token = oauth.auth0.authorize_access_token()
#     session["user"] = token
#     return redirect("/")


# @app.route('/actors/<actor_id>/delete', methods=['POST'])
# @requires_auth(permission='delete:actor')
# def delete_actor(decoded_payload, actor_id):
#   error = False
#   try:
#     record_to_change = Actor.query.get(actor_id)
#     if record_to_change:
#       db.session.delete(record_to_change)
#       db.session.commit()
#       remaining_item = Actor.query.filter(Actor.id > actor_id).all()
#       for item in remaining_item:
#         item.id -= 1
#       db.session.commit()
#   except:
#      db.session.rollback()
#      error = True
#   finally:
#       db.session.close()
#   if error:
#       abort(500)
#   else:
#      actor = Actor.query.all()
#      return render_template('pages/actors.html.html', actor=actor)

@app.route('/actors')
@requires_auth(permission='get:actors')
def actors(decoded_payload):
  data = []
  actor = Actor.query.all()
  return render_template('pages/actors.html', actors=actor)

@app.route('/actors/search', methods=['POST'])
def search_actors():
  search = request.form.get("search_term")
  actors = db.session.query(Actor).filter(Actor.name.ilike(f'%{search}%')).all()
  for i in actors:
    response={
      "count": len(actors),
      "data": [{
        "id": i.id,
        "name": i.name,
        "age": i.age,
         "gender": i.gender
      }]
    }
    print(response)
  return render_template('pages/search_actors.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/actors/<int:actor_id>')
@requires_auth(permission='get:actors')
def show_actor(decoded_payload, actor_id):
  actor = Actor.query.get_or_404(actor_id)
  upcoming_show = []
  past_show= []
  data = vars(actor)
  return render_template('pages/show_actor.html', actor=data)

@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
  form = ActorForm()
  edit_actor = Actor.query.get_or_404(actor_id)
  actor = Actor.query.filter_by(id=actor_id).all()
  for s in actor:
     form.name.data = s.name
     form.age.data = s.age
     form.gender.data = s.gender
  return render_template('forms/edit_actor.html', form=form, actor=edit_actor)

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
@requires_auth(permission='patch:actor')
def edit_actor_submission(decoded_payload, actor_id):
  pre_actor = Actor.query.filter_by(id=actor_id).first()
  form = ActorForm(request.form, meta={'csrf':False})
  if form.validate(): 
    try:
      actor = Actor(id= actor_id, name=form.name.data, age=form.age.data, gender=form.gender.data)
      db.session.delete(pre_actor)
      db.session.commit()
      db.session.add(actor)
      db.session.commit()
    except ValueError as e:
      flash('An error occurred while updating actor ' + request.form['name'])
      db.session.rollback()
    finally:
      flash('Actor ' + request.form['name'] + '  updated successfully.')
      db.session.close()
      return redirect(url_for('show_actor', actor_id=actor_id))
  else:
    validationMessage= []
    for field, errors in form.errors.items():
      for error in errors:
        validationMessage.append(f"{field}:{error}")
  flash('Please fix the errors: '+','.join(validationMessage))
  form=ActorForm()
  return redirect(url_for('edit_actor', actor_id=actor_id))

@app.route('/actors/<int:actor_id>/delete', methods=['POST'])
@requires_auth(permission='delete:actor')
def delete_actor_submission(decoded_payload, actor_id):
  pre_actor = Actor.query.filter_by(id=actor_id).first()
  form = ActorForm(request.form, meta={'csrf':False})
  try:
    db.session.delete(pre_actor)
    db.session.commit()
  except ValueError as e:
    flash('An error occurred while deleting actor ' + request.form['name'])
    db.session.rollback()
  finally:
    flash('Actor ' + request.form['name'] + '  deleted successfully.')
    db.session.close()
    return redirect(url_for('show_actor', actor_id=actor_id))

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
  form = ActorForm()
  print(form.name.data)
  return render_template('forms/new_actor.html', form=form)

@app.route('/actors/create', methods=['POST'])
@requires_auth(permission='post:actor')
def create_actor_submission(decoded_payload):
  form = ActorForm(request.form, meta={'csrf':False})
  movie_id = form.movie_id.data
  isMovieValid = Movie.query.filter_by(id=movie_id).count()
  if(isMovieValid <=0):
    flash('An error occurred.Please check movie id') 
    abort(401)
  else: 
    if form.validate():
      try:
          actor = Actor(name=form.name.data, age=form.age.data, gender=form.gender.data, movie_id = form.movie_id.data)
          db.session.add(actor)
          db.session.commit()
      except ValueError as e:
        print(e)
        db.session.rollback()
      finally:
        db.session.close()
      flash('actor ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')
    else:
      validationMessage= []
      for field, errors in form.errors.items():
          for error in errors:
            validationMessage.append(f"{field}:{error}")
      flash('Please fix the errors: '+','.join(validationMessage))
      form=ActorForm()
      return render_template('forms/new_actor.html', form=form)
  
@app.route('/movies', methods=['GET'])
def get_movie_form():
  data = Movie.query.all()
  return render_template('pages/movie.html', results=data)
  
@app.route('/movies/create', methods=['GET'])
def create_movie_form():
  form = MovieForm()
  return render_template('forms/new_movie.html', form=form)

@app.route('/movies/create', methods=['POST'])
@requires_auth(permission='post:movie')
def create_movie_submission(decoded_payload):
  error = False
  formmovie = MovieForm(request.form, meta={'csrf':False})
  if formmovie.validate():
     try:
        movies = Movie(title=formmovie.title.data,  release_date=formmovie.release_date.data)
        db.session.add(movies)
        db.session.commit()
     except ValueError as e:
        print(e)
        flash('An error occurred. movie ' + request.form['title'] + ' could not be listed.')
        db.session.rollback()
        error = True
        print(sys.exc_info())
     finally:
        db.session.close()
     flash('movie ' + request.form['title'] + ' was successfully listed.')
     return render_template('pages/movie.html')
  else:
     validationMessage= []
     for field, errors in formmovie.errors.items():
        for error in errors:
           validationMessage.append(f"{field}:{error}")
     flash('Please fix the errors: '+','.join(validationMessage))
     form=MovieForm()
     return render_template('forms/new_movie.html', form=form)
          

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    app.run()