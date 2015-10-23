from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from google.appengine.ext import ndb

from modules import User
from api import oauth_server

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = oauth_server.oauth


@app.route('/api/user/me')
@oauth.require_oauth()
def me():
    user_key = request.oauth.access_token.user_id
    user = User.query(User.key == ndb.Key(User, user_key)).fetch(1)[0]
    return jsonify(username=user.username, test='yaya')

