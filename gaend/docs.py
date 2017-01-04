from collections import OrderedDict
from google.appengine.ext import ndb
from flask import request, Response
from gaend import generator
from jinja2 import Environment, FileSystemLoader
from state import APP
import logging

class User(ndb.Model):
    born = ndb.DateTimeProperty()
    name = ndb.StringProperty(choices=['billy', 'bob'])

env = Environment(loader=FileSystemLoader('templates'))

@APP.route('/docs', methods=['GET'])
def docs():
    klasses = OrderedDict([])
    for klass in sorted(ndb.Model._kind_map.values()):
        pd = OrderedDict([])
        for k, p in klass._properties.iteritems():
            prop_klass = p.__class__
            kind = generator.PROPERTIES[prop_klass]
            values = generator.VALUES[kind]
            if p._choices:
                values = p._choices
            pd[k] = {'propClass': p,
                     'vals': values}
        klasses[klass.__name__] = {'modelClass': klass,
                                   'properties': pd}

    return env.get_template('documentation.html').render(klasses=klasses)
