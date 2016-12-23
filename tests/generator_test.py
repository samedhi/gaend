from datetime import date, time, datetime
from google.appengine.ext import testbed, ndb
from gaend.main import app
import itertools
import unittest
import webtest

# References
# cloud.google.com/appengine/docs/python/ndb/db_to_ndb
# cloud.google.com/appengine/docs/python/ndb/entity-property-reference
# cloud.google.com/appengine/docs/python/ndb/creating-entity-models#expando

PROPERTIES = {
    ndb.IntegerProperty: int,
    ndb.FloatProperty: float,
    ndb.BooleanProperty: bool,
    ndb.StringProperty: basestring,
    ndb.TextProperty: basestring,
    ndb.BlobProperty: basestring,
    ndb.DateProperty: date,
    ndb.TimeProperty: time,
    ndb.DateTimeProperty: datetime,
    ndb.GeoPtProperty: ndb.GeoPt,
    ndb.KeyProperty: 'ndb.Key',
    ndb.StructuredProperty: 'ndb.Key',
    ndb.LocalStructuredProperty: 'ndb.Key',
    ndb.JsonProperty: 'serialized',
    ndb.PickleProperty: 'serialized',
    ndb.ComputedProperty: 'computed',
}

# Untested Property Types:
# ndb.BlobKeyProperty - Holdover from `db` days?
# ndb.UserProperty - Google recomends not using this
# ndb.GenericProperty - Why not just use ndb.Expando class?

COMPUTE_FX = lambda x: "COMPUTED_PROPERTY"

class DefaultModel(ndb.Model):
    pass

# Probably wondering why fx instead of just hard coded values? Keys are
# really built with the application_id as part of the key. Because the
# application_id when a test first starts up is different than the
# application_id afterwards, the key will be different in the "compile"
# (first pass) execution of this code than the "runtime" execution of
# this code. Therefore you need to dynamically build the key at
# runtime with a function.
def key_1():
    return ndb.Key('DefaultModel', "DEFAULT_MODEL_NAME_1")
def key_2():
    return ndb.Key('DefaultModel', "DEFAULT_MODEL_NAME_2")

DATETIME_NOW = datetime.now()
DATE_NOW = datetime.now().date()
TIME_NOW = datetime.now().time()

DEFAULTS = {
    bool: False,
    int: 0,
    float: 0.0,
    basestring: "",
    datetime: DATETIME_NOW,
    date: DATE_NOW,
    time: TIME_NOW,
    ndb.GeoPt: ndb.GeoPt(0,0),
    'ndb.Key': key_1,
    'serialized': {},
}

CHOICES = {
    bool: [True, False],
    int: [-1, 0, 1],
    float: [-1.0, 0.0, 1.0],
    basestring: ["", "a", "z"],
    datetime: [DATETIME_NOW],
    date: [DATE_NOW],
    time: [TIME_NOW],
    ndb.GeoPt: [ndb.GeoPt(-1, -1), ndb.GeoPt(0, 0), ndb.GeoPt(1, 1)],
    'ndb.Key': [key_1, key_2],
    'serialized': [{'key1': True, 'key2': []}, {}, [1, 2.0, {}, 'val1']],
}

OPTIONS = {
    'repeated': bool,
    'required': bool,
    'default': DEFAULTS,
    'choices': CHOICES,
}

OPTIONS_KEYS = set([])
# In this pass we are going to build all the combinations of options that
# can be passed to a ndb Property.
for i in range(len(OPTIONS)):
    for options in itertools.combinations(OPTIONS.keys(), i):
        # repeated cannot be combined with required=True or default=True
        if 'repeated' in options:
            options = itertools.ifilterfalse(
                lambda x: x is 'required' or x is 'default',
                options)
            options = tuple(options)
        OPTIONS_KEYS.add(options)

for prop,value in PROPERTIES.items():
    # I am using `.get(k)` instead of `[k]` for `choices` and `default` as
    # some options don't have meaningful values. What is the `defaults` for
    # a `ndb.ComputedProperty` or `ndb.KeyProperty`?
    choices = CHOICES.get(value)
    defaults = DEFAULTS.get(value)
    print value, choices, defaults


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
