from google.appengine.ext import testbed, ndb
import props as gprops


def get(urlsafekey_or_entity):
    """Read a existent entity

    {'kind': <ClassNameOfEntity>,
     'key': <urlsafekey>}

    Returns the above dictionary as a json object where:
    1) All `ndb.Key` entity properties are converted to their urlsafe keys.
    2) All `datetime`, `date`, and `time` objects are converted to iso8601.
    3) Json and Pickled are converted to sub objects or list.
    4) ndb.GeoPt(X,Y) becomes `{'lat': <latitude>, 'lon': <longitude>}`
    5) Every other property is directly copied.
    """
    if isinstance(urlsafekey_or_entity, ndb.Model):
        entity = urlsafekey_or_entity
        assert entity.key, entity
    else:
        key = ndb.Key(urlsafe=urlsafekey)
        entity = key.get()
    return gprops.entity_to_props(entity)


def post(props):
    """Create a new entity

    Validates and then writes the Entity specified by props to the Datastore.

    'kind' is a required key in `props`. The 'kind' field in `props` specifies
    the `ndb.Model` class to be created.

    'key' is a reserved key in `props`. If specified, the entity will be written
    with the provided 'key'. 'key' in `props` should be the urlsafe form of a
    `ndb.Key()` object.


    """
    klass = ndb.Model._lookup_model(props['kind'])
    entity = klass(**props)
    entity.put()
    return get(entity)


def put(urlsafekey, props):
    """Update (Merge) the props into a existent entity

    Transactionally retrieves the entity at `urlsafekey` and then merges
    `props` into the retrieved entity. Next writes the entity into the
    Datastore using the above post() method. In this way all Datastore
    writes always go through the post() method.
    """
    entity = ndb.Key(urlsafe=urlsafekey).get()
    updated_props = gprops.entity_to_props(entity)
    for k, v in props.items():
        updated_props[k] = v
    return post(updated_props)


def delete(urlsafekey):
    """Destroy a entity"""
    ndb.Key(urlsafekey=urlsafekey).delete()
