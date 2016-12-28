from state import APP, MODELS
import endpoint

def add(klass):
    """Add a ndb.Model as a restful endpoint"""
    assert issubclass(klass, ndb.Model), klass
    MODELS[klass.__name__] = klass


def remove(klass):
    """Remove a ndb.Model as a restful endpoint"""
    del MODELS[klass.__name__]
