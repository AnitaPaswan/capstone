
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
    db_drop_and_create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movies = Movie(
        id='1',
        title='Capstone',
        release_date='22/20/2020'
    )
    movies.insert()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    movie_id = Column(db.Integer, db.ForeignKey('movie.id'))

    # Define the relationship
    movie = db.relationship('Movie')
    def __repr__(self):
        return json.dumps(self.short())
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def short(self):
        movie_list = [movie.title for movie in self.movies]
        return {
            "name": self.name,
            "age": self.age,
            "movies": movie_list
        }
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
    def __repr__(self):
        return json.dumps(self.short())
    
    def __init__(self, id, title, release_date):
        self.id = id
        self.title = title
        self.release_date = release_date