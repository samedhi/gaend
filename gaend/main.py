from flask import Flask, jsonify, request
import generator

app = Flask(__name__)
app.config['DEBUG'] = True
