from google.appengine.ext import testbed, ndb
from datetime import datetime, date, time
from dateutil import parser
import copy
import json
import logging

def js_to_ndb(t, v):
    if t is ndb.KeyProperty:
        return ndb.Key(urlsafe=v)
    elif t in [ndb.DateTimeProperty, ndb.DateProperty, ndb.TimeProperty]:
        d = parser.parse(v)
        if t is ndb.DateProperty:
            return date(d.year, d.month, d.day)
        elif t is ndb.TimeProperty:
            return time(d.hour, d.minute, d.second, d.microsecond)
        else:
            return d
    elif t is ndb.GeoPtProperty:
        return ndb.GeoPt(v['lat'], v['lon'])
    elif isinstance(v, basestring):
        return str(v)
    else:
        return v


def ndb_to_js(t, v):
    if t is ndb.KeyProperty:
        return v.urlsafe()
    elif t in [ndb.DateTimeProperty, ndb.DateProperty, ndb.TimeProperty]:
        return v.isoformat()
    elif t is ndb.GeoPtProperty:
        return {'lat': v.lat, 'lon': v.lon}
    else:
        return v


def process_properties(d, fx):
    assert isinstance(d, dict), '%s [%s]' % (d, type(d))
    kind = d['kind']
    klass = ndb.Model._lookup_model(kind)
    for k, v in d.items():
        if k not in ['key', 'kind']:
            p = klass._properties[k]
            t = type(p)
            if type(v) is list:
                vs = v
                new_vs = [fx(t, v) for v in vs]
                d[k] = new_vs
            else:
                d[k] = fx(t, v)


def js_to_props(js):
    """Converts serialized JSON into props

    This converts from a serialized JSON object into a `props` python dict.
    The JSON object requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `js` into Python Objects.
    """
    try:
        js = json.loads(js)
    except ValueError:
        logging.error(js)
        raise
    if 'key' in js:
        js['key'] = ndb.Key(urlsafe=js['key'])
    process_properties(js, js_to_ndb)
    return js


def props_to_js(props):
    """Converts props into serialized JSON

    The converts from a `props` python dict into a serialized JSON object.
    `props` requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `props` into a JSON object.
    """
    props = copy.copy(props)
    if 'key' in props:
        props['key'] = props['key'].urlsafe()
    process_properties(props, ndb_to_js)
    try:
        return json.dumps(props)
    except TypeError:
        logging.error(props)
        raise
