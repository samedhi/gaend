from flask import request
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


@APP.route('/gaend/put/<urlkey>', methods=['GET'])
def puter(urlkey):
    ndb.transaction(lambda: call_every_handler(ON_PUT, request, urlkey),
                    xg=True)
    return "OK"


@APP.route('/gaend/delete/<urlkey>', methods=['GET'])
def deleter(urlkey):
    ndb.transaction(lambda: call_every_handler(ON_DELETE, request, urlkey),
                    xg=True)
    return "OK"
