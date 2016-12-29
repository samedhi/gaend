from google.appengine.ext import testbed, ndb
from datetime import datetime, date, time
import datetutil.parser
import json


def js_to_ndb(t, v):
    if t is ndb.KeyProperty:
        return ndb.Key(urlsafe=v)
    elif t is [ndb.DateTimeProperty, ndb.DateProperty, ndb.TimeProperty]:
        d = dateutil.parser.parse(v)
        if t is ndb.DateProperty:
            return date(d.year, d.month, d.day)
        elif t is ndb.TimeProperty:
            return time(d.hour, d.minute, d.second, d.microsecond)
        else:
            return d
    elif t is ndb.GeoPt:
        return ndb.GeoPt(v['x'], v['y'])
    else:
        return v


def ndb_to_js(t, v):
    if t is ndb.KeyProperty:
        return v.urlsafe()
    elif t is [ndb.DateTimeProperty, ndb.DateProperty, ndb.TimeProperty]:
        return v.isoformat()
    elif t is ndb.GeoPt:
        return {'x': v.x, 'y': v.y}
    else:
        return v


def js_to_props(js):
    """Converts serialized JSON into props

    This converts from a serialized JSON object into a `props` python dict.
    The JSON object requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `js` into Python Objects.
    """
    d = json.loads(js)
    kind = d['kind']
    klass = ndb.Model._lookup_model(kind)
    if 'key' in d:
        d['key'] = ndb.Key(urlsafe=d['key'])
    for k, v in d.items():
        if k not in ['key', 'kind']:
            p = klass._properties[k]
            t = type(p)
            if type(v) is list:
                vs = v
                new_vs = [js_to_ndb(t, v) for v in vs]
                d[k] = new_vs
            else:
                d[k] = js_to_ndb(t, v)

def props_to_js(props):
    """Converts props into serialized JSON

    The converts from a `props` python dict into a serialized JSON object.
    `props` requires a 'kind' key which must specify the class name
    of the Entity it represents. This is necessary as the matching class
    will be queried to determine how to convert the value in the
    (key,value) pairs of `props` into a JSON object.
    """
    pass
