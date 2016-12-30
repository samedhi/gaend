from fixture import GeneratorTest
from google.appengine.ext import testbed, ndb


class GeneratorTest(GeneratorTest):

    def testLotsaModelsGenerated(self):
        for klass in self.klasses:
            k = klass._get_kind()
            assert ndb.Model._lookup_model(k) == klass, klass
