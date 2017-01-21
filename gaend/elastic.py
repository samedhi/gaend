from elasticsearch import Elasticsearch
from flask import abort
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from gaend.props import entity_to_props
from state import APP
import js
import logging


# Specify elasticsearch url with read-write access in `URL`.
URL = None


# NOTES: The tradeoffs of type vs index outlined in following:
# https://www.elastic.co/blog/index-vs-type

# TODO: There are some issues here. What happens if you put
# and then delete; but for whatever reason the task gets executed as
# delete and then put? You would still have a record despite having
# "logically" deleted a records. Versioning entities would logically
# allow you to guarantee order.


def put(urlkey, request):
    taskqueue.add(url='/gaend/elastic/put/%s' % urlkey,
                  method='GET',
                  transactional=True)


def delete(urlkey, request):
    taskqueue.add(url='/gaend/elastic/delete/%s' % urlkey,
                  method='GET',
                  transactional=True)


def elastic():
    return Elasticsearch(hosts=[URL],
                         send_get_body_as='POST',
                         verify_certs=True,
                         ca_certs='/etc/ca-certificates.crt')


@APP.route('/gaend/elastic/put/<urlkey>', methods=['GET'])
def put_elastic(urlkey):
    if not URL:
        logging.error(
            "No ES url specified in `gaend.elastic.URL` [PUT] %s",
            urlkey)
        abort(500)
    es = elastic()
    key = ndb.Key(urlsafe=urlkey)
    entity = key.get()
    prop = entity_to_props(entity)
    doc = js.props_to_js(prop)
    res = es.index(index='gaend',
                   doc_type=prop['kind'],
                   id=prop['key'].urlsafe(),
                   body=doc)
    return "OK"


@APP.route('/gaend/elastic/delete/<urlkey>', methods=['GET'])
def delete_elastic(urlkey):
    if not URL:
        logging.error(
            "No ES url specified in `gaend.elastic.URL` [PUT] %s",
            urlkey)
        abort(500)
    es = elastic()
    key = ndb.Key(urlsafe=urlkey)
    res = es.delete(index='gaend', doc_type=key.kind(), id=urlkey)
    return "OK"
