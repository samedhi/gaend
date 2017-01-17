from google.appengine.ext import ndb
from flask import abort, Flask, request, Response
from state import APP
import endpoint
import js

def validate(props=None, kind=None, urlsafekey=None):
    p_kind = props['kind'].lower() if props and 'kind' in props else None
    kind = kind.lower() if kind else None
    u_kind = ndb.Key(urlsafe=urlsafekey).kind().lower() if urlsafekey else None
    if kind and u_kind and u_kind != kind:
        abort(422,
              "In /<kind>/<urlsafe>, kind != urlsafe.kind()")
    if p_kind and kind and p_kind != kind:
        abort(422,
              "In /<kind>/*, kind != to json-object-body['kind']")
    if p_kind and u_kind and p_kind != u_kind:
        abort(422,
              "In /%s/<urlsafe>, urlsafe.kind() != json-object-body['kind']" %
              kind)
    if props and 'key' in props:
        if props['key'].kind() != props['kind']:
            abort(422,
                  "Json request has a 'key' of kind %s != 'kind' of %s" %
                  (props['key'].kind(), props['kind']))


def jsonify(props):
    json = js.props_to_js(props)
    resp = Response(json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/<kind>/<urlsafekey>', methods=['GET'])
@APP.route('/<urlsafekey>', methods=['GET'])
def get(urlsafekey, kind=None):
    props = endpoint.get(urlsafekey)
    validate(props=props, urlsafekey=urlsafekey, kind=kind)
    return jsonify(props)


@APP.route('/', methods=['POST'])
@APP.route('/<kind>', methods=['POST'])
def post(kind=None):
    validate(kind=kind)
    data = request.data
    props = js.js_to_props(data)
    validate(props=props, kind=kind)
    new_props = ndb.transaction(lambda: endpoint.post(props), xg=True)
    return jsonify(new_props)


@APP.route('/<kind>/<urlsafekey>', methods=['PUT'])
@APP.route('/<urlsafekey>', methods=['PUT'])
def put(urlsafekey, kind=None):
    data = request.data
    props = js.js_to_props(data)
    validate(props=props, urlsafekey=urlsafekey, kind=kind)
    new_props = ndb.transaction(lambda: endpoint.put(props), xg=True)
    return jsonify(new_props)


@APP.route('/<kind>/<urlsafekey>', methods=['DELETE'])
@APP.route('/<urlsafekey>', methods=['DELETE'])
def delete(urlsafekey, kind=None):
    props = endpoint.get(urlsafekey)
    validate(props=props, urlsafekey=urlsafekey, kind=kind)
    ndb.transaction(lambda: endpoint.delete(urlsafekey))
    return jsonify(props)
