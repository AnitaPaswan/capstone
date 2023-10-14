Casting Agency
-----

## Introduction

The Casting Agency models a company that is responsible for model boot caping and managing actor.
As an Executive Producer  we are creating a system to simplify and streamline the process.

Here we build out the data models to power the API endpoints for the Casting Agency site by connecting to a PostgreSQL database for storing, querying, and creating information about actors on Casting Agency.

## Overview

* create actors.
* searching for actors with their id.
* get all actor
* Edit actor


## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` --  Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` --  Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` --  Defines the forms used to create new actors, shows, and movies.
* `app.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` --  Defines the data models that set up the database tables.



## Role Based Access
   
```
Roles:

Casting Assistant(get:actors)
Can view actors

Casting Director(get:actors, post:actor, delete:actor, edit:actor)
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors


Executive Producer(get:actors, get:movies, post:actor, delete:actor, patch:actor, post:movie, delete:movie)
All permissions

```
   
6. **Verify on the Browser**<br>
Navigate to project homepage https://render-capstone-example-5cq7.onrender.com which is homepage once you have login successfull will navigate to view the Casting Agency page.
Logig to below provided cretential

7. User Details
   ##  Casting Director
------------------------------------------------------------
Email : castingDirector@gmail.com 
password : Test1234
   ##  Casting Assistant
------------------------------------------------------------
Email : castingassistant@gmail.com 
password : Test1234

Copy the access token from url 
Sample jwt for Casting Director who has all the access:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1BWW5fdF80X0NXOXkzM09sWFlpOSJ9.eyJpc3MiOiJodHRwczovL2ZzZG4xMjMuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1MjQzY2ZhZTUwMTY0NDM1NGMyN2UyMyIsImF1ZCI6WyJjYXAyIiwiaHR0cHM6Ly9mc2RuMTIzLmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTcyNjgwMDUsImV4cCI6MTY5NzM1NDQwNCwiYXpwIjoidzlXY1ptVkx4OHZuQTZDblc5cHRRNmxhUGk5NW01MVUiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDpob21lIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicG9zdDphY3RvciJdfQ.JKByxwZ0kr_fdv4fsJEZvdnernlsX0WJCHUXn8Ssb9fKO5YV1kIUtkMbihU4yYun-rWgyp56rOTZHsrNYr9nVueL2aJrNjG6VYyApTWjZY3TbbvtuiG-B8UMMW68LMDE8ParPuTczz_4Zp5e-o0aIonUWmh6pijJbxWKqoCe5n9AggCoLPfTt48E84nD3wao461wyI6TwL_AJh7vzX9-zcamnr4OmyUbwVbH11Jyd3OKbtk7xXqEArd4alzmmVdnXU5s0Dhep7mcJSEdrlqGrg4m_fX2z7hVDOViasIGGqeQWc5ElVp0WFP7IDuRw9n1DKnhHqyyxD2ja-IkWRjgqQ







