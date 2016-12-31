from fixture import GeneratorTest
from google.appengine.ext import testbed, ndb
import gaend.generator as generator
import gaend.props as gprops
import re


class PropsTest(GeneratorTest):

    def testEntityToPropsAndBack(self):
        for klass in self.klasses:
            # Create entity1 of this klass
            kind = klass._get_kind()
            # 'BlobPropertyRepeatedModel' -> 'Blob'
            prop_name = re.match(r'(.+)Property', kind).group(1)
            prop_name = prop_name[0].lower() + prop_name[1:] + 'Property'
            prop_klass = klass._properties[prop_name].__class__
            prop_type = generator.PROPERTIES[prop_klass]
            for v in generator.VALUES[prop_type]:
                # Convert everything to a list so that can write single
                # code path for values that need to be computed (like
                # ndb.Key). Then un-list non repeated items.
                if re.search('Repeated', klass._get_kind()):
                    v = [v]
                else:
                    v = generator.VALUES[prop_type]
                for i, fx in enumerate(v):
                    if callable(fx):
                        v[i] = fx()
                if not re.search('Repeated', klass._get_kind()):
                    v = v[0]

                # Unpersisted
                entity1 = klass(**{prop_name:v})
                props = gprops.entity_to_props(entity1)
                entity2 = gprops.props_to_entity(props)
                assert entity1 == entity2

                # Persisted
                entity3 = klass(**{prop_name:v})
                entity3.put()
                props = gprops.entity_to_props(entity3)
                entity4 = gprops.props_to_entity(props)
                assert entity3 == entity4
