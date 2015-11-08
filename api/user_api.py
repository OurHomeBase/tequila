'''Api for User profile'''

from flask import request
from flask import jsonify

from persistence import user_models
from api import oauth_api
from flask_httpauth import HTTPBasicAuth
from persistence import oauth_models
from flask import abort

from api import common

# pylint: disable=invalid-name
app = common.create_flask_app()
basic_auth = HTTPBasicAuth()
oauth = oauth_api.oauth
# pylint: disable=invalid-name


@basic_auth.get_password
def get_pw(username):
  client = oauth_models.Client.find_by_client_id(username)

  return client.client_secret if client else None

@app.route('/api/user/', methods=['POST'])
@basic_auth.login_required
def CreateUser():
  '''Registers a new user.'''
  if not request.json:
    abort(400)

  username = request.json['username']
  user = user_models.User.find_by_username(username)
  if not user:
    user = user_models.User(username=username)
    user.put()

  return jsonify(username=username)


@app.route('/api/user/me')
@oauth.require_oauth()
def me():
  user_id = request.oauth.access_token.user_id
  user = user_models.User.find_by_id(user_id)
  return jsonify(username=user.username, test='yaya')

@app.route('/api/user/she')
def she():
  '''Test method without auth restriction.'''
  return jsonify(test='yaya')
