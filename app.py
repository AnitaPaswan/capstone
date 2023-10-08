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

app = Flask(__name__)
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)
setup_db(app)
cors = CORS(app)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
# @app.after_request
# def after_request(response):
#   response.headers.add("Access-Control-Allow-Headers","ContentType, Authorization")
#   response.headers.add("Access-Control-Allow-Methods", "GET, DELETE,POST, PATCH")
#   return response


@app.route('/')
def index():
  return render_template('pages/home.html')


#  movies
#  ----------------------------------------------------------------
@app.route('/movies')
def movies():
  # TODO: replace with real movies data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per movie.

  dataDb=movie.query.all()
 
  return render_template('pages/movies.html', areas=dataDb)

# Anita-GET movie code for create movie end

@app.route('/movies/search', methods=['POST'])
def search_movies():
  response = {}
  data = {}
  data1 = []
  search = request.form.get("search_term")
  movie = db.session.query(movie).filter(movie.name.ilike(f'%{search}%')).all()
  for i in movie:
    data['name']=i.name
    if i.name not in data1:
     data1.append(data)
  response['count']=len(movie)
  response['data']= data1
  print(response)
  return render_template('pages/search_movies.html', results=response, search_term=request.form.get('search_term', ''))

#Anita movie byid start
@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
  # shows the movie page with the given movie_id
  # TODO: replace with real movie data from the movies table, using movie_id
  #Implement Past and incoming shows
  movie = movie.query.get_or_404(movie_id)
  past_shows=[]
  upcoming_shows=[]
  for show in movie.shows:
    print(movie.shows)
    temp_show={
       'actor_id':show.actor_id,
       'actor_name':show.actor.name,
       'actor_image_link': show.actor.image_link,
       'start_time':show.start_time.strftime("%m/%d/%Y, %H:%M")
       }
    if show.start_time<=datetime.now():
       past_shows.append(temp_show)
    else:
      upcoming_shows.append(temp_show)
  data = vars(movie)
  data['past_shows']=past_shows
  data['upcoming_shows']=upcoming_shows
  data['past_shows_count']=len(past_shows),
  data['upcoming_shows_count']=len(upcoming_shows)
  return render_template('pages/show_movie.html', movie=data)

@app.route('/movies/create', methods=['GET'])
def create_movie_form():
  form = movieForm()
  return render_template('forms/new_movie.html', form=form)

@app.route('/movies/create', methods=['POST'])
def create_movie_submission():
  error = False
  formmovie = movieForm(request.form, meta={'csrf':False})
  if formmovie.validate():
     try:
        movies = movie(title=formmovie.title.data,  release_date=formmovie.release_date.data)
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
     return render_template('pages/home.html')
  else:
     validationMessage= []
     for field, errors in formmovie.errors.items():
        for error in errors:
           validationMessage.append(f"{field}:{error}")
     flash('Please fix the errors: '+','.join(validationMessage))
     form=movieForm()
     return render_template('forms/new_movie.html', form=form)

@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
  error = False
  try:
      movie = movie.query.filter_by(id = movie_id)
      for x in movie:
          db.session.delete(x)
      db.session.delete(movie)
      db.session.commit()
  except:
     db.session.rollback()
     error = True
  finally:
      db.session.close()
  if error:
      abort(500)
  else:
     return None

@app.route('/actors')
def actors():
  data = actor.query.all()

  return render_template('pages/actors.html', actors=data)

@app.route('/actors/search', methods=['POST'])
def search_actors():
  search = request.form.get("search_term")
  actors = db.session.query(actor).filter(actor.name.ilike(f'%{search}%')).all()
  for i in actors:
    show = Show.query.filter_by(actor_id=i.id).all()
    response={
      "count": len(actors),
      "data": [{
        "id": i.id,
        "name": i.name,
        "num_upcoming_shows": len(show),
      }]
    }
    print(response)
  return render_template('pages/search_actors.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):
  actor = actor.query.get_or_404(actor_id)
  upcoming_show = []
  past_show= []
  data = vars(actor)
  for show in actor.shows:
     temp_show={
     'movie_id':show.movie_id,
     'movie_name':show.movie.name,
     'movie_image_link': show.movie.image_link,
     'start_time':show.start_time.strftime("%m/%d/%Y, %H:%M")
     }
     if show.start_time<=datetime.now():
        past_show.append(temp_show)
     else:
        upcoming_show.append(temp_show)
  data = vars(actor)
  data['past_shows']=past_show
  data['upcoming_shows']=upcoming_show
  data['past_shows_count']=len(past_show),
  data['upcoming_shows_count']=len(upcoming_show)
  return render_template('pages/show_actor.html', actor=data)

@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
  form = actorForm()
  edit_actor = actor.query.get_or_404(actor_id)
  actor = actor.query.filter_by(id=actor_id).all()
  for s in actor:
     form.name.data = s.name
     form.city.data = s.city
     form.genres.data = s.genres
     form.state.data = s.state
     form.phone.data = s.phone
     form.website_link.data = s.website_link
     form.facebook_link.data = s.facebook_link
     form.seeking_movie.data = s.seeking_movie
     form.seeking_description.data = s.seeking_description
     form.image_link.data = s.image_link
  return render_template('forms/edit_actor.html', form=form, actor=edit_actor)

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):
  pre_actor = actor.query.filter_by(id=actor_id).first()
  form = actorForm(request.form)
  if form.validate(): 
    try:
      actor = actor(id= actor_id, name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data, genres=form.genres.data, facebook_link=form.facebook_link.data, image_link=form.image_link.data, website_link=form.website_link.data, seeking_movie=form.seeking_movie.data, seeking_description=form.seeking_description.data)
      db.session.delete(pre_actor)
      db.session.commit()
      db.session.add(actor)
      db.session.commit()
    except ValueError as e:
      flash('An error occurred while updating actor ' + request.form['name'])
      db.session.rollback()
    finally:
      flash('actor ' + request.form['name'] + '  updated successfully.')
      db.session.close()
      return redirect(url_for('show_actor', actor_id=actor_id))
  else:
    validationMessage= []
    for field, errors in form.errors.items():
      for error in errors:
        validationMessage.append(f"{field}:{error}")
  flash('Please fix the errors: '+','.join(validationMessage))
  form=actorForm()
  return redirect(url_for('edit_actor', actor_id=actor_id))

@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):
  form = movieForm()
  edit_movie = movie.query.get_or_404(movie_id)
  movie = movie.query.filter_by(id=movie_id).all()
  for ven in movie:
    form.name.data = ven.name
    form.city.data = ven.city
    form.genres.data = ven.genres
    form.address.data = ven.address
    form.state.data = ven.state
    form.phone.data = ven.phone
    form.website_link.data = ven.website_link
    form.facebook_link.data = ven.facebook_link
    form.seeking_talent.data = ven.seeking_talent
    form.seeking_description.data = ven.seeking_description
    form.image_link.data = ven.image_link
  return render_template('forms/edit_movie.html', form=form, movie=edit_movie)

@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):
  pre_movie = movie.query.filter_by(id=movie_id).first()
  formmovie = movieForm(request.form, meta={'csrf':False})
  if formmovie.validate(): 
    try:
      ven = movie(id=movie_id, name=formmovie.name.data, city=formmovie.city.data, state=formmovie.state.data, address=formmovie.address.data, phone=formmovie.phone.data, genres=formmovie.genres.data, facebook_link=formmovie.facebook_link.data,image_link=formmovie.image_link.data, website_link=formmovie.website_link.data, seeking_talent=formmovie.seeking_talent.data, seeking_description=formmovie.seeking_description.data)
      db.session.delete(pre_movie)
      db.session.commit()
      db.session.add(ven)
      db.session.commit()
    except ValueError as e:
      flash('An error occurred while updating movie ' + request.form['name'])
      db.session.rollback()
    finally:
      flash('movie ' + request.form['name'] + '  updated successfully.')
      db.session.close()
      return redirect(url_for('show_movie', movie_id=movie_id))
  else:
    validationMessage= []
    for field, errors in formmovie.errors.items():
      for error in errors:
        validationMessage.append(f"{field}:{error}")
  flash('Please fix the errors: '+','.join(validationMessage))
  form=movieForm()
  return redirect(url_for('edit_movie', movie_id=movie_id))

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
  form = actorForm()
  return render_template('forms/new_actor.html', form=form)

@app.route('/actors/create', methods=['POST'])
def create_actor_submission():
  form= actorForm(request.form, meta={'csrf':False})
  if form.validate():
    try:
        actor = actor(name=form.name.data, age=form.age.data, gender=form.gender.data)
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
     form=actorForm()
     return render_template('forms/new_actor.html', form=form)
          

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
