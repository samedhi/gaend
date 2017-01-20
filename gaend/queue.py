from google.appengine.ext import ndb
from state import APP


# If you don't want gaend to use the default queue, override the
# GAEND_QUEUE variable.
GAEND_QUEUE = 'default'

# This is a list of functions that will be called in the task queue
# when a datastore record is added/updated.
ON_PUT = []

# This is a list of functions that will be called in the task queue
# when a datastore record is deleted.
ON_DELETE = []


def call_every_handler(handlers, request, urlkey):
    for fx in handlers:
        fx(urlkey, request)


@APP.route('/gaend/put/<urlkey>', methods=['POST'])
def puter():
    ndb.transaction(lambda: call_every_handler(ON_MODIFY, urlkey, request),
                    xg=True)
    return 200


@APP.route('/gaend/delete/<urlkey>', methods=['POST'])
def deleter():
    ndb.transaction(lambda: call_every_handler(ON_DELETE, urlkey, request),
                    xg=True)
    return 200
