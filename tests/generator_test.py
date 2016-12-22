from datetime import date, time, datetime
from google.appengine.ext import testbed, ndb
from gaend.main import app
import unittest
import webtest

# References
# cloud.google.com/appengine/docs/python/ndb/db_to_ndb
# cloud.google.com/appengine/docs/python/ndb/entity-property-reference
# cloud.google.com/appengine/docs/python/ndb/creating-entity-models#expando

PROPERTIES = [
    ndb.IntegerProperty, # [int],
    ndb.FloatProperty, # [float],
    ndb.BooleanProperty, # [bool],
    ndb.StringProperty, # [(basestring, lambda x, #  len(s) < 1500)],
    ndb.TextProperty, # [basetring]
    ndb.BlobProperty, # [basestring],
    ndb.DateProperty, # [date],
    ndb.TimeProperty, # [time],
    ndb.DateTimeProperty, # [datetime],
    ndb.GeoPtProperty, # [ndb.GeoPt],
    ndb.KeyProperty, # [ndb.Model],
    ndb.StructuredProperty, # [ndb.Model]
    ndb.LocalStructuredProperty, # [ndb.Model],
    ndb.JsonProperty, # python list or dict
    ndb.PickleProperty # python list or dict
]

# Untested Property Types
# 1. ndb.BlobKeyProperty - Holdover from `db` days?
# 2. ndb.UserProperty - Google recomends not using this
# 3. ndb.ExpandoProperty - Why not just use ndb.Expando class?
# 4. ndb.GenericProperty - Why not just use ndb.Expando class?

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
