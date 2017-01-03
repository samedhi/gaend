from google.appengine.ext import ndb
from flask import request, Response
from gaend import generator
from jinja2 import Environment, FileSystemLoader
from state import APP
import logging

class User(ndb.Model):
    name = ndb.DateTimeProperty()
    email = ndb.StringProperty()

env = Environment(loader=FileSystemLoader('templates'))

@APP.route('/docs', methods=['GET'])
def docs():
    o = {}
    for klass in ndb.Model._kind_map.values():
        pd = {}
        for k, p in klass._properties.iteritems():
            klass = p.__class__
            kind = generator.PROPERTIES[klass]
            values = generator.VALUES[kind]
            logging.error(values)
            pd[k] = {'propClass': p,
                     'vals': values}
        o[klass.__name__] = {'modelClass': klass,
                             'properties': pd}

    return env.get_template('documentation.html').render(klasses=o)
