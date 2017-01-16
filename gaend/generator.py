from datetime import date, time, datetime
from google.appengine.ext import testbed, ndb
import itertools
import logging

# References
# cloud.google.com/appengine/docs/python/ndb/db_to_ndb
# cloud.google.com/appengine/docs/python/ndb/entity-property-reference
# cloud.google.com/appengine/docs/python/ndb/creating-entity-models#expando


# This is the compute fx passed to a ndb.ComputedProperty
def compute_fx(self):
    return "COMPUTED_PROPERTY"


# These are the Models used for ndb.Key's as well as
# ndb.StructuredProperty and ndb.LocalStructuredProperty
# class PetModel(ndb.Model):
#     name = ndb.StringProperty(default="Fido")


# class TestModel(ndb.Model):
#     pet = ndb.KeyProperty(kind=PetModel)


# Probably wondering why fx instead of just hard coded values? Keys are
# really built with the application_id as part of the key. Because the
# application_id when a test first starts up is different than the
# application_id afterwards, the key will be different in the "compile"
# (first pass) execution of this code than the "runtime" execution of
# this code. Therefore you need to dynamically build the key at
# runtime with a function.
def key_1():
    return ndb.Key('TestModel', "DEFAULT_MODEL_NAME_1")


def key_2():
    return ndb.Key('TestModel', "DEFAULT_MODEL_NAME_2")


# This is all the ndb.*Property under test. A few Properties were not tested
# as they seemed depreciated or unecessary. Note that ndb.ComputedProperty is
# included in the set of classes for each property in ./tests/generator_test.py
#
# Untested Property Types:
# ndb.BlobKeyProperty - Holdover from `db` days?
# ndb.UserProperty - Google recomends not using this
# ndb.GenericProperty - Why not just use ndb.Expando class?
#
# DEV NOTE: I remain unconvinced that ndb.*StructuredProperty are worth their
# added mental complexity. I feel that you would almost always be better off
# creating additional full fledged entities and then refering to them by key.
# Unless your application has substantial performance or data size constraints,
# I feel that anything that can be done with a structured property can more
# understandably be done with multiple writes with transactions.
# tldr; I have chosen not to test them, but will be happy to accept pull request
# that do!
# ndb.StructuredProperty - NOT TESTED
# ndb.LocalStructuredProperty - NOT TESTED
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
    ndb.JsonProperty: 'serialized',
    ndb.PickleProperty: 'serialized',
}

DATETIME_NOW = datetime.now()
DATE_NOW = datetime.now().date()
TIME_NOW = datetime.now().time()

# Default values for property of the given 'type'. If a property has
# default=<value> then <value> will be pulled from this DEFAULTS dictionary.
DEFAULTS = {
    bool: False,
    int: 0,
    float: 0.0,
    basestring: "",
    datetime: DATETIME_NOW,
    date: DATE_NOW,
    time: TIME_NOW,
    ndb.GeoPt: ndb.GeoPt(0, 0),
    'ndb.Key': key_1,
    'serialized': {},
}

# Possible choices of values for the property of the given type. If a property
# has a choices=<list-of-choices> then <list-of-choices> will be pulled for
# this CHOICES dictionary.
CHOICES = {
    bool: [True, False],
    int: [-1, 0, 1],
    float: [-1.0, 0.0, 1.0],
    basestring: ['do', 're', 'mi'],
    datetime: [DATETIME_NOW],
    date: [DATE_NOW],
    time: [TIME_NOW],
    ndb.GeoPt: [ndb.GeoPt(-1, -1), ndb.GeoPt(0, 0), ndb.GeoPt(1, 1)],
    'ndb.Key': [key_1, key_2],
}

# CHOICES and VALUES differ only in that values contains the additional
# 'serialized' key/value pair. 'serialized' cannot be provided as a `choice`
# as `nd.Model.__init__` require that all arguments to `choice` be put
# in a frozenset...
VALUES = {'serialized': [{'key1': True, 'key2': []},
                         {},
                         [1, 2.0, {}, 'val1']]}
for k, v in CHOICES.items():
    VALUES[k] = v

# The options that are passed to a ndb.Property(). Note that not all options
# can be passed to every ndb.Property(). As an example, 'computed' type can
# have neither a `default` or a `choices` option, so it is not included in
# the dictionary above.
OPTIONS = {
    'repeated': bool,
    'required': bool,
    'default': DEFAULTS,
    'choices': CHOICES,
}

# This is a set of all the different combinations of options that can be passed
# to a ndb.Property().
OPTION_KEYS = set([])
for i in range(len(OPTIONS)):
    for options in itertools.combinations(OPTIONS.keys(), i):
        # repeated cannot be combined with required=True or default=True, so if
        # we have `repeated` in a set we can take out both of them.
        if 'repeated' in options:
            options = itertools.ifilterfalse(
                lambda x: x is 'required' or x is 'default',
                options)
            options = tuple(options)
        OPTION_KEYS.add(options)
OPTION_KEYS = sorted(OPTION_KEYS)
