from flask import Flask, jsonify, request
from google.appengine.ext import testbed, ndb
import props

def post(props):
    """Create a new entity

    Validates and then writes the Entity specified by props to the Datastore.

    'kind' is a required key in `props`. The 'kind' field in `props` specifies
    the `ndb.Model` class to be created.

    'key' is a reserved key in `props`. If specified, the entity will be written
    with the provided 'key'. 'key' in `props` should be the urlsafe form of a
    `ndb.Key()` object.


    """
    pass


def get(urlsafekey):
    """Read a existent entity

    {'kind': <ClassNameOfEntity>,
     'key': <urlsafekey>}

    Returns the above dictionary as a json object where:
    1) All `ndb.Key` entity properties are converted to their urlsafe keys.
    2) All `datetime`, `date`, and `time` objects are converted to iso8601.
    3) Json, Pickled, and *Structured are converted to sub-dictionaries.
    4) ndb.GeoPt(X,Y) are converted to `{'x': X, 'y': Y}`
    5) Every other property is directly copied.

    """
    pass


def put(urlsafekey, props):
    """Update (Merge) the props into a existent entity

    Transactionally retrieves the entity at `urlsafekey` and then merges
    `props` into the retrieved entity. Next writes the entity into the
    Datastore using the above post() method. In this way all Datastore
    writes always go through the post() method.
    """
    pass


def delete(urlsafekey):
    """Destroy a entity"""
    pass
