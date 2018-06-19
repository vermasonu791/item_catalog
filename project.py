# <----Imports---->
from flask import Flask, render_template, request, redirect
from flask import Flask, url_for, flash, jsonify, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Base, Category, CategoryItem, User

# <----Import for creating loging session---->
from flask import session as login_session
from functools import wraps
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# <----Flask Object---->
app = Flask(__name__)

# <----creating client id---->
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Game info app"

# <----Connect to the database---->
engine = create_engine('sqlite:///gamedb.db')
Base.metadata.bind = engine


# <----creating session---->
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()


# <----Loging routing and create anti-forgery state token---->
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# <----GConnect---->
@app.route('/gconnect', methods=['POST'])
def gconnect():

    # <----Validate state token---->
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # <----Obtain authorization code, now compatible with Python3---->
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # <----Upgrade the authorization code into a credentials object---->
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # <----Check that the access token is valid.---->
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)

    # <----Submit request, parse response - Python3 compatible---->
    h = httplib2.Http()
    req = h.request(url, 'GET')[1]
    req_json = req.decode('utf8').replace("'", '"')
    result = json.loads(req_json)

    # <----If there was an error in the access token info, abort.---->
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # <----Verify that the access token is used for the intended user.---->
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # <----Verify that the access token is valid for this app---->
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # <----Store the access token in the session for later use.---->
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # <----Get user info---->
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # <----see if user exists, if it doesn't make a new one---->
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# <----User Helper Functions---->


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# <----gdisconnect method---->


@app.route('/gdisconnect')
def gdisconnect():

        # <----Only disconnect a connected user---->
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':

        # <----Reset the user's sesson.---->
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showAllCat'))
        flash("You are now logged out.")
        return response
    else:

        # <----For whatever reason, the given token was invalid.---->
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# <----Retrive JSON text format---->


@app.route('/categories/<int:category_id>/game/JSON')
def gameinfoJSON(category_id):
    gameinfo = session.query(Category).filter_by(id=category_id).one()
    items = session.query(
                          CategoryItem).filter_by(
                          category_id=category_id).all()
    return jsonify(CategoryItem=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/game/<int:game_id>/JSON')
def menuItemJSON(category_id, game_id):
    gameItem = session.query(CategoryItem).filter_by(id=game_id).one()
    return jsonify(CategoryItem=gameItem.serialize)

# <----Routing to Homepage---->


@app.route('/')
@app.route('/categories/')
def showAllCat():
    game = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        flash("You need to login first for viewing the game")
        return render_template('publicinfo.html', game=game)
    else:
        return render_template('allgametype.html', game=game)


# <----Category of games---->
@app.route('/categories/<int:category_id>/')
def showitems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    if 'username' not in login_session:
        flash("for perforing create delete" +
              " edit or update you need to login first ")
        return render_template('publicgam' +
                               'einfo.html', category=category, item=items)
    else:
        return render_template('inside' +
                               'type.html', category=category, item=items)


# <----Create route for and newgame function---->
@app.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
def newGame(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newgame = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               category_id=category_id,
                               user_id=login_session['user_id'])
        session.add(newgame)
        session.commit()
        flash("New Game has been created")
        return redirect(url_for('showitems', category_id=category_id))
    else:
        return render_template('newgame.html', category_id=category_id)


# <----Create route for and editGame function---->
@app.route('/categories/<int:category_id>' +
           '/<int:game_id>/edit/', methods=['GET', 'POST'])
def editGame(category_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedgame = session.query(CategoryItem).filter_by(id=game_id).one()
    if editedgame.user_id != login_session['user_id']:
     return "<script>function myFunction(){alert('You are not authorized to edit \
       this restaurant. please create your own restaurant in order to edit.');} \
       </script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedgame.name = request.form['name']
        if request.form['description']:
            editedgame.description = request.form['description']
        session.add(editedgame)
        session.commit()
        flash("New Game has been edited")
        return redirect(url_for('showitems', category_id=category_id))
    else:
        return render_template('e' +
                               'ditgame' +
                               '.html',
                               category_id=category_id,
                               game_id=game_id, item=editedgame)

# <----Create a route for and deleteGame function---->


@app.route('/categories/' +
           '<int:category_id>/<int:game_id>/delete/', methods=['GET', 'POST'])
def deleteGame(category_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CategoryItem).filter_by(id=game_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("game has been deleted")
        return redirect(url_for('showitems', category_id=category_id))
    else:
        return render_template('deletegame.html', item=itemToDelete)

# <----Debug---->
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
