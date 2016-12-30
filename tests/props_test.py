from gaend.state import APP
from google.appengine.ext import testbed, ndb
import fixture
import unittest
import webtest


class PropsTest(unittest.TestCase):

    def setUp(self):
        self.testapp = webtest.TestApp(APP)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.klasses = fixture.all_props_combination()

    def tearDown(self):
        self.testbed.deactivate()

    def testLotsaModelsGenerated(self):
        for klass in self.klasses:
            k = klass._get_kind()
            assert ndb.Model._lookup_model(k) == klass, klass
