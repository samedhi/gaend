from flask import Flask, jsonify, request
import endpoint
import js


def get(urlsafekey):
    props = endpoint.get(urlsafekey)
    json = js.props_to_js(props)
    resp = flask.Response(json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@ndb.transactional(xg=True)
def put(json):
    props = js.js_to_props(json)
    return endpoint.put(props)


@ndb.transactional(xg=True)
def post(json):
    props = js.js_to_props(json)
    return endpoint.post(props)


def delete(urlsafekey):
    endpoint.delete(urlsafekey)
    return "SUCCESS"
