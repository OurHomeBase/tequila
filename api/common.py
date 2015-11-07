'''Stores common objects for api.'''

from flask import Flask
from flask_oauthlib.provider import OAuth2Provider

# pylint: disable=invalid-name
app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
app.config['DEBUG'] = True
# pylint: disable=invalid-name

oauth = OAuth2Provider(app)
