from flask import Flask, jsonify, request
import endpoint
import js


@APP.route('/<model>/<urlsafekey>', methods=['GET'])
@APP.route('/<urlsafekey>', methods=['GET'])
def get(urlsafekey):
    props = endpoint.get(urlsafekey)
    json = js.props_to_js(props)
    resp = flask.Response(json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/<model>/<urlsafekey>', methods=['PUT'])
@APP.route('/<urlsafekey>', methods=['PUT'])
@ndb.transactional(xg=True)
def put(json):
    props = js.js_to_props(json)
    return endpoint.put(props)


@APP.route('/<model>', methods=['POST'])
@APP.route('/', methods=['POST'])
@ndb.transactional(xg=True)
def post(json):
    props = js.js_to_props(json)
    return endpoint.post(props)


@APP.route('/<model>/<urlsafekey>', methods=['DELETE'])
@APP.route('/<urlsafekey>', methods=['DELETE'])
def delete(model, urlsafekey):
    endpoint.delete(urlsafekey)
    return "SUCCESS"
