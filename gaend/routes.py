from google.appengine.ext import ndb
from flask import Flask, request, Response
from state import APP
import endpoint
import js


def jsonify(props):
    json = js.props_to_js(props)
    resp = Response(json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/', methods=['GET'])
def index():
    return "Index page for this whole site"


@APP.route('/<model>/<urlsafekey>', methods=['GET'])
@APP.route('/<urlsafekey>', methods=['GET'])
def get(urlsafekey, model=None):
    props = endpoint.get(urlsafekey)
    return jsonify(props)


@APP.route('/', methods=['POST'])
@APP.route('/<model>', methods=['POST'])
def post(model=None):
    data = request.data
    props = js.js_to_props(data)
    new_props = ndb.transaction(lambda: endpoint.post(props), xg=True)
    return jsonify(new_props)


@APP.route('/<model>/<urlsafekey>', methods=['PUT'])
@APP.route('/<urlsafekey>', methods=['PUT'])
def put(urlsafekey, model=None):
    data = request.data
    props = js.js_to_props(data)
    new_props = ndb.transaction(lambda: endpoint.put(props), xg=True)
    return jsonify(new_props)


@APP.route('/<model>/<urlsafekey>', methods=['DELETE'])
@APP.route('/<urlsafekey>', methods=['DELETE'])
def delete(urlsafekey, model=None):
    props = endpoint.get(urlsafekey)
    ndb.transaction(lambda: endpoint.delete(urlsafekey))
    return jsonify(props)
