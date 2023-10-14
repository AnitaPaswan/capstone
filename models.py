
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
    movie_detail = recipe = Column(String(180), nullable=False)

    # Define the relationship
    movie = db.relationship('Movie')
    def __repr__(self):
        return json.dumps(self.short())
    
    def short(self):
        movie_data = json.loads(self.movie_detail)
        # Extract specific information from each movie and store as a list of dictionaries
        short_name = [{'title': movie['title'], 'release_date': movie['release_date']} for movie in movie_data]
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_detail': short_name  # Include the list of movie details
        }
    
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    def __repr__(self):
        return f'<movie ID: {self.id}, title: {self.title}, release_date: {self.release_date}>'
    
    
