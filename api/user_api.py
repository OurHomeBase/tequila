from flask import Flask
from flask import request
from flask import jsonify

from persistence import models
from api import oauth_server

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = oauth_server.oauth


@app.route('/api/user/me')
@oauth.require_oauth()
def me():
    user_id = request.oauth.access_token.user_id
    user = models.User.findById(user_id)
    return jsonify(username=user.username, test='yaya')

