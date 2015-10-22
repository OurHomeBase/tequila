# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from google.appengine.ext import ndb


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'

app.config['DEBUG'] = True

oauth = OAuth2Provider(app)


class User(ndb.Model):
    #id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    
    @property
    def id(self):
        if self.key:
            return self.key.id()
        else:
            return None
                                                                 


class Client(ndb.Model):
    client_id = ndb.StringProperty()
    client_secret = ndb.StringProperty()

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

    p_redirect_uris = ndb.StringProperty()
    p_defaultscopes = ndb.StringProperty()

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self.p_redirect_uris:
            return self.p_redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.p_redirect_uris[0]

    @property
    def default_scopes(self):
        if self.p_defaultscopes:
            return self.p_defaultscopes.split()
        return []


class Grant(ndb.Model):
    id = ndb.IntegerProperty()

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

    client_id = ndb.StringProperty()
    client = ndb.StructuredProperty(Client)

    code = ndb.StringProperty()

    redirect_uri = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    p_scopes = ndb.StringProperty()

    def delete(self):
        self.key.delete()
        return self

    @property
    def scopes(self):
        if self.p_scopes:
            return self.p_scopes.split()
        return []


class Token(ndb.Model):
    id = ndb.IntegerProperty()
    client_id = ndb.StringProperty()
    client = ndb.StructuredProperty(Client)

    user_id = ndb.IntegerProperty()
    user = ndb.StructuredProperty(User)

    # currently only bearer is supported
    token_type = ndb.StringProperty()

    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()
    expires = ndb.DateTimeProperty()

    p_scopes = ndb.StringProperty()

    @property
    def p_user(self):
        return self.user
        
    @property
    def scopes(self):
        if self.p_scopes:
            return self.p_scopes.split()
        return []


def current_user():
    if 'id' in session:
        uid = session['id']
        qry = User.query(User.id == uid)
        users = qry.fetch(1)
        return users[0]
    
    return None


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user_list = User.query(User.username == username).fetch(1)
        if user_list:
            user = user_list[0]
        else:    
            user = User(username=username)
            user.put()
        session['id'] = user.id
        return redirect('/s/')
    user = current_user()
    return render_template('home.html', user=user)
    

CLIENT_ID = 'GbRmKgbSMmlE2NlugMeFfQIba8hoVyBFsWS8Igsq'
CLIENT_SECRET = 'BfP7jsN8dSsXjGLfTTPiEvarMJOpkZQ2Y7IVVee8X929LfolMV'

@app.route('/client')
def client():
    user = current_user()
    if not user:
        return redirect('/s/')
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        redirect_uris=' '.join([
            'http://localhost:8080/c/authorized',
            'http://127.0.0.1:8080/c/authorized',
            'http://127.0.1:8080/c/authorized',
            'http://127.1:8080/c/authorized',
            ]),
        defaultscopes='email',
        user_id=user.id,
    )
    item.put()
    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )

@app.route('/createClient')
def createClient():
    client_list = Client.query(Client.client_id == CLIENT_ID).fetch(1)
    if client_list:
        client = client_list[0]
    else:
        client = Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            p_redirect_uris=' '.join([
                'http://localhost:8080/c/authorized',
                'http://127.0.0.1:8080/c/authorized',
                'http://127.0.1:8080/c/authorized',
                'http://127.1:8080/c/authorized',
                ]),
            p_defaultscopes='email',
        )
        client.put()
    return jsonify(
        client_id=client.client_id,
        client_secret=client.client_secret,
    )



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


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user_key = request.oauth.access_token.user_id
    user = User.query(User.key == ndb.Key(User, user_key)).fetch(1)[0]
    return jsonify(username=user.username, test='yaya')

