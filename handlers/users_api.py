from flask import Flask, Blueprint, render_template, redirect, url_for
from flask import session as login_session
from database import session, User
import random
import string

users_api = Blueprint('users_api', __name__)

# User Helper Functions
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

def getCurrentUser():
    if 'user_id' in login_session:
        return login_session['user_id']
    else:
        return None

def validUserPermission(user_id):
    if getCurrentUser() == user_id:
        return True
    else:
        return False

# Create anti-forgery state token and display login.
@users_api.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@users_api.route('/logout')
def showLogout():
    return redirect(url_for('gconnect_api.gdisconnect'))

