'''Stores common objects for api.'''

from flask import Flask
from persistence import oauth_models
from flask_httpauth import HTTPBasicAuth


basic_auth = HTTPBasicAuth() # pylint: disable=invalid-name

def create_flask_app():
  '''Creates a configured flask app.'''
  app = Flask(__name__, template_folder='templates')
  app.debug = True
  app.secret_key = 'secret'
  app.config['DEBUG'] = True

  return app

def get_user_id(request):
  '''Gets user id from request.'''
  return request.oauth.access_token.user_id

@basic_auth.get_password
def get_client_secret(client_id):
  client = oauth_models.Client.find_by_client_id(client_id)

  return client.client_secret if client else None
