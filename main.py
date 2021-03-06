import sys
sys.path.insert(0, sys.path[0] + '/models')
sys.path.insert(0, sys.path[1] + '/handlers')

from flask import Flask
from database import session, Category, Item
from base import render_template

from json_api import json_api
from items_api import items_api
from category_api import category_api
from users_api import users_api
from gconnect_api import gconnect_api

app = Flask(__name__)

app.register_blueprint(json_api)
app.register_blueprint(items_api)
app.register_blueprint(category_api)
app.register_blueprint(users_api)
app.register_blueprint(gconnect_api)

@app.route('/')
@app.route('/index')
def Main():
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(3)
    return render_template('main.html', latest_items=latest_items)

if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

