from fixture import GeneratorTest
from google.appengine.ext import testbed, ndb
import gaend.generator as generator
import re


class PropsTest(GeneratorTest):

    def testEntityToPropsAndBack(self):
        for klass in self.klasses:
            # Create entity1 of this klass
            kind = klass._get_kind()
            # 'BlobPropertyRepeatedModel' -> 'Blob'
            prop_name = re.match(r'(.+)Property', kind).group(1)
            prop_name = prop_name[0].lower() + prop_name[1:]
            prop_klass = klass._properties[prop_name + 'Property'].__class__
            prop_type = generator.PROPERTIES[prop_klass]
            for v in generator.VALUES[prop_type]:
                print v

            # Convert entity1 to props form
            # Create entity2 derived from props
            # Assure that first entity1 is equal to entity2
