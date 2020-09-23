import os
import time
import requests
from requests.auth import HTTPDigestAuth as HTTPAuth
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret key'

auth = HTTPDigestAuth()

users={"vcu": "rams"}

@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None
    
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Page Not Found'}), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Servier Error'}), 500

@app.route('/ping', methods=['GET'])
@auth.login_required
def ping():
    startTime = time.time()
    url = 'https://cmsc455-cordovaom-pong.herokuapp.com/pong'
    pongAuth = HTTPAuth('vcu', 'rams')
    pongRequest = requests.get(url, auth= pongAuth)
    return jsonify((time.time() - startTime)*1000), 200