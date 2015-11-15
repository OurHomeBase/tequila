from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from google.appengine.ext import ndb

from persistence import oauth_models
from persistence import user_models
from utils import constants

from api import oauth_api

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = oauth_api.oauth

@app.route('/api/client/janet')
def janet():
  user = user_models.User(username="janet@ourhomebase.co")
  user.timeProfile = user_models.TimeProfile(workStatus="Full Time")
  user.addresses = {'home':user_models.Address(city='Amsterdam'), 'work':user_models.Address(city='SF'), }
  user.put()
  
  user1 = user_models.User.findByUsername("janet@ourhomebase.co")
  
  return user1.findAddressByType('home').city


@app.route('/api/client/create')
def createClient():
  client = oauth_models.Client.findByClientId(constants.CLIENT_ID)
  if not client:
    client = oauth_models.Client(
        client_id=constants.CLIENT_ID,
        client_secret=constants.CLIENT_SECRET,
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


