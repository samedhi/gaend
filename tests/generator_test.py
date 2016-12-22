from datetime import date, time, datetime
from google.appengine.ext import testbed, ndb
from gaend.main import app
import unittest
import webtest

# References
# cloud.google.com/appengine/docs/python/ndb/db_to_ndb
# cloud.google.com/appengine/docs/python/ndb/entity-property-reference
# cloud.google.com/appengine/docs/python/ndb/creating-entity-models#expando

SERIALIZE = [{'key1': True, 'key2': []}, [1, 2.0, {}, 'json']]

COMPUTED = lambda x: "COMPUTED_PROPERTY"

PROPERTIES = {
    ndb.IntegerProperty: [int],
    ndb.FloatProperty: [float],
    ndb.BooleanProperty: [bool],
    ndb.StringProperty: [(basestring, lambda x:  len(s) < 1500)],
    ndb.TextProperty: [basestring],
    ndb.BlobProperty: [basestring],
    ndb.DateProperty: [date],
    ndb.TimeProperty: [time],
    ndb.DateTimeProperty: [datetime],
    ndb.GeoPtProperty: [ndb.GeoPt],
    ndb.KeyProperty: [ndb.Model],
    ndb.StructuredProperty: [ndb.Model],
    ndb.LocalStructuredProperty: [ndb.Model],
    ndb.JsonProperty: SERIALIZE,
    ndb.PickleProperty: SERIALIZE,
    ndb.ComputedProperty: COMPUTED,
}

# Untested Property Types:
# ndb.BlobKeyProperty - Holdover from `db` days?
# ndb.UserProperty - Google recomends not using this
# ndb.GenericProperty - Why not just use ndb.Expando class?

class DefaultModel(ndb.Model):
    pass

DEFAULTS = {
    bool: False,
    int: 0,
    float: 0.0,
    basestring: "",
    ndb.GeoPt: ndb.GeoPt(0,0),
    ndb.Model: DefaultModel,
}

CHOICES = {
    bool: [True, False],
    int: [-1, 0, 1],
    float: [-1.0, 0.0, 1.0],
    basestring: "",
    ndb.GeoPt: ndb.GeoPt(0,0),
    ndb.Model: DefaultModel,
}

PROPERTY_OPTIONS = {
    'indexed': bool,
    'repeated': bool,
    'required': bool,
    'default': DEFAULTS,
    'choices': CHOICES,
}

class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testTruthItself(self):
        assert True
