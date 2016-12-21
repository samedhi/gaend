from flask import jsonify
from flask import request
from flask import Flask
from google.appengine.ext import ndb

app = Flask(__name__)
app.config['DEBUG'] = True  # Jim says put on safety
