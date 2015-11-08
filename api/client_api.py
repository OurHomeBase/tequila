'''A module to create OAuth client. It helps with integration testing.'''

from flask import jsonify

from persistence import oauth_models
from utils import constants
from api import common

app = common.create_flask_app() # pylint: disable=invalid-name


@app.route('/api/client/create')
def create_client():
  '''Creates a test client or returns an existing one.'''
  client = oauth_models.Client.find_by_client_id(constants.CLIENT_ID)
  if not client:
    client = oauth_models.Client(client_id=constants.CLIENT_ID,
                                 client_secret=constants.CLIENT_SECRET)

    client.put()

  return jsonify(
      client_id=client.client_id,
      client_secret=client.client_secret)
