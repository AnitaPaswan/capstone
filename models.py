
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

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    movie_id = Column(db.Integer, db.ForeignKey('movie.id'))

    # Define the relationship
    movie = db.relationship('Movie')
    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender,
        self.movie_id = movie_id
    def short(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def short(self):
        return {
            'title': self.title,
            'release_date': self.release_date
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
