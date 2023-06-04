import threading

from flask_sqlalchemy import SQLAlchemy
import requests 

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.jokes import initJokes
from model.users import initUsers
from model.players import initPlayers


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api


# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://pranavs31899:v2_45K26_Dzp25fLpvn69SDw7fPnZiCk@db.bit.io:5432/pranavs31899/HelperX'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return str(self.id)
# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/',methods = ["POST", "GET"])  # connects default URL to index() function
def index():
    if request.method == "Post":
        db.add(users(username="Samarth",score=request.form["score"]))
        db.session.commit()


    return render_template("index.html")


@app.before_first_request
def activate_job():  # activate these items 
    initJokes()
    initUsers()
    initPlayers()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8086")
