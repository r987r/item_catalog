from flask import Flask, Blueprint, render_template
from flask import session as login_session
import random
import string

users_api = Blueprint('users_api', __name__)

# Create anti-forgery state token
@users_api.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

