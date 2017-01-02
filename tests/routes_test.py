from fixture import GeneratorTest
from google.appengine.ext import testbed, ndb
import gaend.generator as generator
import gaend.props as gprops
import gaend.js as gjs
import re


class PropsTest(GeneratorTest):

    def testEndpoints(self):
        for klass in self.klasses:
            kind = klass._get_kind()
            prop_name = re.match(r'(.+)Property', kind).group(1)
            prop_name = prop_name[0].lower() + prop_name[1:] + 'Property'
            prop_klass = klass._properties[prop_name].__class__
            prop_type = generator.PROPERTIES[prop_klass]
            first_value = generator.VALUES[prop_type][0]
            last_value = generator.VALUES[prop_type][-1]

            if callable(first_value):
                first_value = first_value()
            if callable(last_value):
                last_value = last_value()
            if re.search('Repeated', klass._get_kind()):
                first_value = [first_value]
                last_value = [last_value]

            post = self.testapp.post_json(
                '/' + kind.lower(),
                gjs.props_to_js({'kind': kind, prop_name: first_value}))

            key = post['key']

            get1 = self.testapp.get('/' + kind.lower() + '/' + key)
            assert js.js_to_props(get1)[prop_name] == first_value

            put = self.testapp.put_json(
                '/' + kind.lower() + '/' + key,
                gjs.props_to_js({'kind': kind, prop_name: last_value}))
            assert post['key'] == put['key']

            get2 = self.testapp.get('/' + kind.lower() + '/' + key)
            assert js.js_to_props(get2)[prop_name] == last_value

            delete = self.testapp.delete('/' + kind.lower() + '/' + key)
            assert get2 == delete

            get3 = self.testapp.get('/' + kind.lower() + '/' + key)
            assert get3 == None



            for v in generator.VALUES[prop_type]:
                # Convert everything to a list so that can write single
                # code path for values that need to be computed (like
                # ndb.Key). Then un-list non repeated items.


                # Unpersisted
                entity1 = klass(**{prop_name:v})
                props1 = gprops.entity_to_props(entity1)
                js = gjs.props_to_js(props1)
                props2 = gjs.js_to_props(js)
                entity2 = gprops.props_to_entity(props2)
                assert entity1 == entity2

                # Persisted
                entity3 = klass(**{prop_name:v})
                props3 = gprops.entity_to_props(entity3)
                js = gjs.props_to_js(props3)
                props4 = gjs.js_to_props(js)
                entity4 = gprops.props_to_entity(props4)
                assert entity3 == entity4
