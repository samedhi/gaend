from collections import OrderedDict
from datetime import datetime
from google.appengine.ext import ndb
from flask import request, Response
from gaend import generator, js
from jinja2 import Environment, PackageLoader
from state import APP
import json
import logging

# class User(ndb.Model):
#     male = ndb.BooleanProperty(default=True)
#     born = ndb.DateTimeProperty()
#     time = ndb.TimeProperty(repeated=True)
#     date = ndb.DateProperty(required=True)
#     age = ndb.IntegerProperty(default=42)
#     height = ndb.FloatProperty(default=23.34)
#     name = ndb.StringProperty(default='bob', choices=['billy', 'bob'])

env = Environment(loader=PackageLoader('gaend', 'templates'))

@APP.route('/docs', methods=['GET'])
def docs():
    klasses = OrderedDict([])
    for klass in sorted(ndb.Model._kind_map.values(), key=lambda k: k.__name__):
        if klass.__name__ == 'GaendFullModel':
            continue
        pd = OrderedDict([])
        for k, p in klass._properties.iteritems():
            prop_klass = p.__class__
            if prop_klass in [ndb.ComputedProperty]:
                continue
            kind = generator.PROPERTIES[prop_klass]
            values = generator.VALUES[kind]
            if p._choices:
                values = p._choices
            values = list(values)
            for i, v in enumerate(values):
                if callable(v):
                    values[i] = v = values[i]()
                values[i] = js.ndb_to_js(prop_klass, v)
                values[i] = json.dumps(values[i])
            default = None
            if p._default:
                default = js.ndb_to_js(prop_klass, p._default)
                default = json.dumps(default)
            pd[k] = {'propClass': p,
                     'vals': values,
                     'default': default}
        klasses[klass.__name__] = {'modelClass': klass,
                                   'properties': pd}

    return env.get_template('documentation.html').render(klasses=klasses)
