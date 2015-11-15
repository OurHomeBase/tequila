'''A module to implement password OAuth Grant and authentication.'''

from datetime import datetime
from datetime import timedelta

from flask_oauthlib.provider import OAuth2Provider

from persistence import user_models
from persistence import oauth_models

from api import app_utils

app = app_utils.create_flask_app() # pylint: disable=invalid-name
oauth = OAuth2Provider(app) # pylint: disable=invalid-name



@oauth.clientgetter
def load_client(client_id):
  return oauth_models.Client.find_by_client_id(client_id)


@oauth.grantgetter
def load_grant(client_id, code):
  return oauth_models.Grant.find_by_client_id_and_code(client_id, code)

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs): # pylint: disable=unused-argument
  '''Saves grant in the DB.'''
  # decide the expires time yourself
  expires = datetime.utcnow() + timedelta(seconds=100)

  grant = oauth_models.Grant(
      client_id=client_id,
      code=code['code'],
      scopes=[request.scopes],
      expires=expires)
  grant.put()

  return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
  if access_token:
    return oauth_models.Token.find_by_access_code(access_token)
  elif refresh_token:
    return oauth_models.Token.find_by_refresh_code(refresh_token)


# pylint: disable=unused-argument
@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
  '''Saves token to DB in association with the user.'''
  old_tokens = oauth_models.Token.find_all_by_client_user_id(
      request.client.client_id, request.user.id)
  # make sure that every client has only one token connected to a user
  for old_token in old_tokens:
    old_token.key.delete()

  expires_in = token.pop('expires_in')
  expires = datetime.utcnow() + timedelta(seconds=expires_in)
  user = oauth_models.OAuthUser(id=request.user.id)

  token = oauth_models.Token(
      access_token=token['access_token'],
      refresh_token=token['refresh_token'],
      token_type=token['token_type'],
      scopes=[token['scope']],
      expires=expires,
      client_id=request.client.client_id,
      user_id=request.user.id,
      user=user)

  token.put()

  return token
# pylint: enable=unused-argument


@app.route('/oauth/token', methods=['GET', 'POST'])
@app_utils.basic_auth.login_required
@oauth.token_handler
def token_handler():
  return None

# pylint: disable=unused-argument
@oauth.usergetter
def get_user(username, password, client, request, *args, **kwargs):
  if not client:
    return None
  user = user_models.User.find_by_username(username)
#   if not user.validate_password(password):
#     return None

  return oauth_models.OAuthUser(id=user.key.id())
# pylint: enable=unused-argument
