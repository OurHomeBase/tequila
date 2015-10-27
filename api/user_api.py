from flask import Flask
from flask import request
from flask import jsonify

from persistence import user_models
from api import oauth_api

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = oauth_api.oauth


@app.route('/api/user/me')
@oauth.require_oauth()
def me():
  user_id = request.oauth.access_token.user_id
  user = user_models.User.findById(user_id)
  return jsonify(username=user.username, test='yaya')

@app.route('/api/user/she')
def she():
  '''Test method without auth restriction.'''
  return jsonify(test='yaya')
