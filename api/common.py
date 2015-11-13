'''Stores common objects for api.'''

from flask import Flask

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
