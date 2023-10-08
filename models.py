
import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    db.app = app
    db.init_app(app)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    shows = db.relationship('Show', backref='movie', lazy='joined', cascade='all, delete')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __init__(self, id,title,release_date):
        self.id=id
        self.title=title
        self.release_date=release_date

    def __iter__(self):
       yield from{
           "id":self.id,
          "title":self.title,
          "release_date":self.release_date
       }.items()
    def __str__(self):
       return json.dumps(dict(self), ensure_ascii=False)
    def __repr__(self):
       return self.__str__()
        # return f'<movie ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link},facebook_link: {self.facebook_link}, website_link: {self.website_link}, seeking_description: {self.seeking_description}, seeking_talent: {self.seeking_talent},  genres: {self.genres}>'

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    shows = db.relationship('Show',backref='actor', lazy='joined', cascade='all, delete')
    def __repr__(self):
        return f'<actor ID: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and actor models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    movie_id =  db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    def __repr__(self):
        return f'<Show ID: {self.id}, movie_id: {self.movie_id}, actor_id: {self.actor_id}, start_time: {self.start_time}>'

