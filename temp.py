
from flask_pymongo import PyMongo, MongoClient  # pip install Flask pymongo
import yaml  # pip install pyyaml, store MYSQL 
from flask import Flask, render_template, url_for, request, session, redirect,flash  # create virtualenv to install Flask

app = Flask(__name__)


with open(r'db.yaml') as file: # Copy relative path
    dbpass=yaml.load(file, Loader=yaml.FullLoader)
    app.config['MONGO_URI'] = dbpass['uri']
    # app.config['SECRET_KEY'] = dbpass['secret_key']
client = MongoClient(app.config['MONGO_URI'])

# Define the database name 
db = client.web_app
mongo = PyMongo(app)

db.users.insert_one({'name': 'jerry'})