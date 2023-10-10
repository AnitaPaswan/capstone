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


