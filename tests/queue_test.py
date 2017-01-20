from fixture import GeneratorTest
from google.appengine.ext import ndb
from gaend.models import GaendFullModel
import gaend.js as gjs

class TaskQueueTest(GeneratorTest):

    def testModelPutAndDelete(self):
        kind = GaendFullModel.__name__
        post = self.testapp.post(
            '/' + kind,
            gjs.props_to_js({'kind': kind}),
            content_type='application/json')
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(
            tasks[0].url, '/gaend/put/%s' % post.json['key'])

        delete = self.testapp.delete('/' + kind + '/' + post.json['key'])
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(
            tasks[1].url, '/gaend/delete/%s' % post.json['key'])
