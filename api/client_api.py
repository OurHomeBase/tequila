from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from google.appengine.ext import ndb

from persistence import models

from api import oauth_server

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = oauth_server.oauth


CLIENT_ID = 'GbRmKgbSMmlE2NlugMeFfQIba8hoVyBFsWS8Igsq'
CLIENT_SECRET = 'BfP7jsN8dSsXjGLfTTPiEvarMJOpkZQ2Y7IVVee8X929LfolMV'

@app.route('/api/client/create')
def createClient():
    client = models.Client.findByClientId(CLIENT_ID)
    if not client:
        client = models.Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            p_redirect_uris=' '.join([
                'http://localhost:8080/c/authorized',
                'http://127.0.0.1:8080/c/authorized',
                'http://127.0.1:8080/c/authorized',
                'http://127.1:8080/c/authorized',
                ]),
            p_defaultscopes='email',
        )
        client.put()
    return jsonify(
        client_id=client.client_id,
        client_secret=client.client_secret,
    )


