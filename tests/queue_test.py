from fixture import GeneratorTest
from google.appengine.ext import ndb
from gaend.models import GaendFullModel
from gaend.queue import ON_PUT, ON_DELETE
import gaend.js as gjs

class TaskQueueTest(GeneratorTest):

    def puter(self):
        kind = GaendFullModel.__name__
        return self.testapp.post(
            '/' + kind,
            gjs.props_to_js({'kind': kind}),
            content_type='application/json')

    def deleter(self):
        kind = GaendFullModel.__name__
        return self.testapp.delete('/' + kind + '/' + self.key)


    def testModelPutAndDelete(self):
        post = self.puter()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 1)
        self.key = post.json['key']
        self.assertEqual(tasks[0].url, '/gaend/put/%s' % self.key)

        delete = self.deleter()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1].url, '/gaend/delete/%s' % self.key)

    def testModelPutAndDeleteSideEffects(self):
        k = ndb.Key(GaendFullModel.__name__, "testing")
        ON_PUT.append(lambda a, b: GaendFullModel(key=k).put())
        post = self.puter()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        get = self.testapp.get(tasks[0].url)
        assert k.get()

        ON_DELETE.append(lambda a, b: k.delete())
        self.key = post.json['key']
        delete = self.deleter()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        get = self.testapp.get(tasks[1].url)
        assert k.get() == None
