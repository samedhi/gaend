from google.appengine.ext import testbed, ndb
import json


def js_to_props(js):
    """Converts serialized JSON into props

    This converts from a serialized JSON object into a `props` python dict.
    The JSON object requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `js` into Python Objects.
    """
    pass


def props_to_js(props):
    """Converts props into serialized JSON

    The converts from a `props` python dict into a serialized JSON object.
    `props` requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `props` into a JSON object.
    """
    pass
