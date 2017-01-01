from flask import Flask, request
from state import APP
import endpoint
import js


def jsonify(props):
    json = js.props_to_js(props)
    resp = flask.Response(json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/<model>/<urlsafekey>', methods=['GET'])
@APP.route('/<urlsafekey>', methods=['GET'])
def get(urlsafekey):
    props = endpoint.get(urlsafekey)
    return jsonify(props)


@APP.route('/<model>', methods=['POST'])
@APP.route('/', methods=['POST'])
@ndb.transactional(xg=True)
def post(json):
    props = js.js_to_props(json)
    new_props = endpoint.post(props)
    return jsonify(new_props)


@APP.route('/<model>/<urlsafekey>', methods=['PUT'])
@APP.route('/<urlsafekey>', methods=['PUT'])
@ndb.transactional(xg=True)
def put(json):
    props = js.js_to_props(json)
    new_props = endpoint.put(props)
    return jsonify(new_props)


@APP.route('/<model>/<urlsafekey>', methods=['DELETE'])
@APP.route('/<urlsafekey>', methods=['DELETE'])
def delete(model, urlsafekey):
    props = endpoint.get(urlsafekey)
    endpoint.delete(urlsafekey)
    return jsonify(props)
