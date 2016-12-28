from flask import Flask, jsonify, request

APP = Flask(__name__)
APP.config['DEBUG'] = True

MODELS = {}
