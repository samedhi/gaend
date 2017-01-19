from elasticsearch import Elasticsearch
from flask import abort
from google.appengine.ext import ndb
import js
import logging

# Specify elasticsearch url with read-write access in `URL`.
URL = None

# NOTES: The tradeoffs of type vs index outlined in following:
# https://www.elastic.co/blog/index-vs-type

def put(urlsafe):
    if not URL:
        logging.error(
            "No ES url specified in `gaend.elastic.URL` [PUT] %s",
            prop['key'])
        abort(500)
    es = Elasticsearch(hosts=[URL], verify_certs=True)
    key = ndb.Key(urlsafe=urlsafe)
    entity = k.get()
    prop = entity_to_props(entity)
    doc = js.prop_to_js(prop)
    logging.error(doc)
    logging.error(URL)
    # res = es.index(index='gaend', doc_type=prop['kind'], id=prop['key'], body=doc)



def delete(urlsafe):
    if not URL:
        logging.error(
            "No ES url specified in `gaend.elastic.URL` [PUT] %s",
            prop['key'])
        abort(500)
    es = Elasticsearch(hosts=[URL], verify_certs=True)
    # res = es.delete(index='gaend', doc_type=prop['kind'], id=prop['key'])
