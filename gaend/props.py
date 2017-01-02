from google.appengine.ext import testbed, ndb
import copy


def entity_to_props(entity):
    """Converts a Datastore Entity into props

    Converts a ndb.Model Entity into its props form. The props form
    contains all of the properties within the entity as a dict. The props
    form also contains a 'kind' that points to the string form
    of the matching class. The `props` form also contains a 'key'
    that contains the entity.key() object.
    """
    d = entity.to_dict()
    if entity.key:
        d['key'] = entity.key
    d['kind'] = entity._get_kind()
    return d


def props_to_entity(props):
    """Converts props into a Datastore Entity

    Converts from a `props` python dict into a `ndb.Model` Entity.

    `props` requires a 'kind' key which must specify the class name
    of the Entity it represents.

    If props contains 'key', the keyed Entity will be retrieved from
    the Datastore and will be used as the the Entity Object. Otherwise
    a new Entity will be created from the matching 'kind' class.

    `props` (without the 'kind' key) will then be passed as the arguments
    to the newly constructed Entity.
    """
    kind = props['kind']
    klass = ndb.Model._lookup_model(kind)
    props = copy.copy(props)
    del props['kind']
    entity = klass(**props)
    return entity
