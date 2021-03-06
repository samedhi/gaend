from gaend.main import APP
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed, ndb
from gaend.models import GaendFullModel, GaendReadMixin, GaendWriteMixin
import gaend.generator as generator
import unittest
import webtest


def all_props_combination():
    """The set of classes representing all Property combinations

    This function returns a mathematical combination of classes, where each
    class is made of exactly one Property and zero or more options. The classes
    are named `<PropertyKind>Property<CamelCased-Sorted-Option-Keys>Model`. So
    a `ndb.KeyProperty` with `choices` and `default` as option would have a
    class name of `KeyPropertyDefaultChoicesModel`. A `ndb.StringProperty` with
    no options would have a class name of `StringPropertyModel`.
    """
    ps = []
    for prop, kind in generator.PROPERTIES.items():
        # I am using `.get(k)` instead of `[k]` for `choices` and `default` as
        # some options don't have meaningful values. As an example, what is the
        # `defaults` for a `ndb.ComputedProperty` or `ndb.KeyProperty`?
        choices = generator.CHOICES.get(kind)
        default = generator.DEFAULTS.get(kind)

        # The `callable` stuff is a goofy hack to deal with the keys not having
        # the right application_id at compile time vs runtime. Basically, if we
        # see that something is a function rather than data, we will call the
        # function to get a value for the data.
        for options in generator.OPTION_KEYS:
            key_names = sorted([k.capitalize() for k in options])
            klass_name = prop.__name__ + "".join(key_names) + 'Model'
            prop_name = prop.__name__[0].lower() + prop.__name__[1:]
            o = {}
            if choices and 'choices' in options:
                choices = list(choices)
                for i, x in enumerate(choices):
                    if callable(x):
                        choices[i] = x()
                o['choices'] = choices
            if default and 'default' in options:
                if callable(default):
                    default = default()
                o['default'] = default
            if 'required' in options:
                o['required'] = True
            if 'repeated' in options:
                o['repeated'] = True

            if prop == ndb.StructuredProperty or \
               prop == ndb.LocalStructuredProperty:
                p = prop(generator.PetModel, **o)
            else:
                p = prop(**o)
            klass = type(klass_name, (GaendFullModel,), {prop_name: p})
            ps.append(klass)

    # Very Strange. ndb.ComputedProperty will let you pass
    # only repeated and indexed as additional. I am not really
    # clear what repeated does... Bit wastfull, but just passing
    # the most basic compute fx regardless of options.
    # p = ndb.ComputedProperty(generator.compute_fx)
    # klass = type('ComputedPropertyModel', (ndb.Model,), {'computedProperty': p})
    # ps.append(klass)
    return ps


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.testapp = webtest.TestApp(APP)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.klasses = all_props_combination()

    def tearDown(self):
        self.testbed.deactivate()
