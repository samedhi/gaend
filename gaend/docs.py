from google.appengine.ext import ndb
from flask import request, Response
from jinja2 import Environment, FileSystemLoader
from state import APP

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()

env = Environment(loader=FileSystemLoader('templates'))

@APP.route('/docs', methods=['GET'])
def docs():
    o = {}
    for klass in ndb.Model._kind_map.values():
        o[klass.__name__] = klass._properties

    return env.get_template('documentation.html').render(klasses=o)
