from fixture import GeneratorTest
from google.appengine.ext import ndb
from gaend.models import GaendFullModel
from gaend.queue import ON_PUT, ON_DELETE
import gaend.elastic as gelastic
import gaend.js as gjs
import os

class ElasticTest(GeneratorTest):

    def setUp(self):
        GeneratorTest.setUp(self)
        ON_PUT.append(gelastic.put)
        ON_DELETE.append(gelastic.delete)
        # Be sure to set your elasticsearch write url as environment variable
        # `$ export ELASTICSEARCH_WRITE_URL=<YOUR_ELASTICSEARCH_URL>`
        assert 'ELASTICSEARCH_WRITE_URL' in os.environ
        gelastic.URL = os.environ['ELASTICSEARCH_WRITE_URL']

    def tearDown(self):
        GeneratorTest.tearDown(self)
        del ON_PUT[:]
        del ON_DELETE[:]

    def puter(self):
        kind = GaendFullModel.__name__
        return self.testapp.post(
            '/' + kind,
            gjs.props_to_js({'kind': kind}),
            content_type='application/json')

    def deleter(self):
        kind = GaendFullModel.__name__
        return self.testapp.delete('/' + kind + '/' + self.key)

    def testElasticPutAndDelete(self):
        k = ndb.Key(GaendFullModel.__name__, "testing")
        post = self.puter()

        # This is the put task firing
        task_url = self.taskqueue_stub.get_filtered_tasks()[-1].url
        self.assertEqual(task_url, '/gaend/put/%s' % post.json['key'])
        get = self.testapp.get(task_url)

        # print map(lambda x: x.url, self.taskqueue_stub.get_filtered_tasks())

        # This is the elastic put task firing
        task_url = self.taskqueue_stub.get_filtered_tasks()[-1].url
        self.assertEqual(task_url, '/gaend/elastic/put/%s' % post.json['key'])
        get = self.testapp.get(task_url)



    #     delete = self.deleter()
    #     tasks = self.taskqueue_stub.get_filtered_tasks()
    #     # This is the delete task firing
    #     get = self.testapp.get(tasks[-1].url)
    #     # This is the elastic delete task firing
    #     get = self.testapp.get(tasks[-1].url)
