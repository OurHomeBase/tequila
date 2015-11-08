'''Stores common objects for api.'''

from flask import Flask

def create_flask_app():
  app = Flask(__name__, template_folder='templates')
  app.debug = True
  app.secret_key = 'secret'
  app.config['DEBUG'] = True

  return app
