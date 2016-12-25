from google.appengine.ext import testbed, ndb
from gaend.main import app, generator
from gaend.generator import DEFAULTS, CHOICES, OPTION_KEYS, PROPERTIES
import unittest
import webtest

for prop,kind in PROPERTIES.items():
    # I am using `.get(k)` instead of `[k]` for `choices` and `default` as
    # some options don't have meaningful values. What is the `defaults` for
    # a `ndb.ComputedProperty` or `ndb.KeyProperty`?
    choices = CHOICES.get(kind)
    default = DEFAULTS.get(kind)

    # This is a goofy hack to deal with the keys not having the right
    # application_id at compile time vs runtime.
    if choices:
        for i,x in enumerate(choices):
            if callable(x):
                choices[i] = x()

    if default and callable(default):
        default = default()

    for options in OPTION_KEYS:
        klass_name = prop.__name__ + 'Model'
        prop_name = prop.__name__[0].lower() + prop.__name__[1:]
        o = {}
        if choices and 'choices' in options:
            o['choices'] = choices
        if default and 'default' in options:
            o['default'] = default
        if 'required' in options:
            o['required'] = True
        if 'repeated' in options:
            o['repeated'] = True

        if prop == ndb.StructuredProperty or \
           prop == ndb.LocalStructuredProperty:
            p = prop(generator.PetModel, **o)
        elif prop == ndb.ComputedProperty:
            # Very Strange. ndb.ComputedProperty will let you pass
            # only repeated and indexed as additional. I am not really
            # clear what repeated does... Bit wastfull, but just passing
            # the most basic compute fx regardless of options.
            p = prop(generator.COMPUTE_FX)
        else:
            p = prop(**o)
        klass = type(klass_name, (ndb.Model,), {prop_name: p})
        # print klass, kind, default, choices


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
