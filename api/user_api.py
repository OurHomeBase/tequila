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

  username = request.json['username']
  user = user_models.User.find_by_username(username)
  if not user:
    user = user_models.User(username=username)
    user.put()

  return jsonify(username=username, user_id=user.key.id())


@app.route('/api/user/me')
@oauth_api.oauth.require_oauth()
def get_user():
  user_id = app_utils.get_user_id(request)
  user = user_models.User.find_by_id(user_id)
  return jsonify(username=user.username, test='yaya')
