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

            post = self.testapp.post(
                '/' + kind.lower(),
                gjs.props_to_js({'kind': kind, prop_name: first_value}),
                content_type='application/json')
            key = post.json['key']

            get1 = self.testapp.get('/' + kind.lower() + '/' + key)
            get_value = gjs.js_to_props(get1.normal_body)[prop_name]
            assert get_value == first_value, get1.normal_body

            updated = {'kind': kind,
                       'key': ndb.Key(urlsafe=post.json['key']),
                       prop_name: last_value}
            put = self.testapp.put(
                '/' + kind.lower() + '/' + key,
                gjs.props_to_js(updated),
                content_type='application/json')
            assert post.json['key'] == put.json['key']

            get2 = self.testapp.get('/' + kind.lower() + '/' + key)
            get_value =  gjs.js_to_props(get2.normal_body)[prop_name]
            assert get_value == last_value, get1.normal_body

            delete = self.testapp.delete('/' + kind.lower() + '/' + key)
            assert get2.normal_body == delete.normal_body

            get3 = self.testapp.get(
                '/' + kind.lower() + '/' + key,
                expect_errors=404)
