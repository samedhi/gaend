from flask import jsonify
from flask import request
from flask import Flask
from google.appengine.ext import ndb

import generator

app = Flask(__name__)
app.config['DEBUG'] = True
