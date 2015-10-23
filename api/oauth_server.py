# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from google.appengine.ext import ndb

from modules import User
from modules import Client
from modules import Grant
from modules import Token

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = OAuth2Provider(app)



@oauth.clientgetter
def load_client(client_id):
    qry = Client.query(Client.client_id == client_id)
    clients = qry.fetch(1)
    return clients[0]


@oauth.grantgetter
def load_grant(client_id, code):
    qry = Grant.query(Grant.client_id == client_id, Grant.code==code)
    grants = qry.fetch(1)
    return grants[0]


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        p_scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    grant.put()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query(Token.access_token == access_token).fetch(1)[0]
    elif refresh_token:
        return Token.query(Token.refresh_token == refresh_token).fetch(1)[0]


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query(
        Token.client_id==request.client.client_id,
        Token.user_id==request.user.id
    ).fetch()
    # make sure that every client has only one token connected to a user
    for t in toks:
        t.key.delete()

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        p_scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    tok.put()
    return tok


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect('/s/')
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query(Client.client_id == client_id).fetch(1)[0]
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@oauth.usergetter
def get_user(username, password, client, request, *args, **kwargs):
    # client: current request client
#     if not client.has_password_credential_permission:
#         return None
#     user = User.get_user_by_username(username)
#     if not user.validate_password(password):
#         return None
    user = User.query(User.username == username).fetch(1)[0]
    
    return user

    
    # parameter `request` is an OAuthlib Request object.
    # maybe you will need it somewhere
#    return user


