'''Api for User profile'''

from flask import request
from flask import jsonify

from persistence import user_models
from api import oauth_api
from flask import abort

from api import app_utils

app = app_utils.create_flask_app() # pylint: disable=invalid-name


@app.route('/api/user/', methods=['POST'])
@app_utils.basic_auth.login_required
def create_user():
  '''Registers a new user.'''
  if not request.json:
    abort(400)

  email = request.json['email']
  password = request.json['password']

  user = user_models.User.find_by_email(email)
  if not user:
    user = user_models.User.create(email, password)
    user.put()

  return jsonify(email=email, user_id=user.key.id())


@app.route('/api/user/me')
@oauth_api.oauth.require_oauth()
def get_user():
  user_id = app_utils.get_user_id(request)
  user = user_models.User.find_by_id(user_id)
  return jsonify(email=user.email)


@app.route('/api/user/', methods=['DELETE'])
@oauth_api.oauth.require_oauth()
def delete_user():
  user_id = app_utils.get_user_id(request)
  user = user_models.User.find_by_id(user_id)
  user.key.delete()

  return jsonify(success=True)
