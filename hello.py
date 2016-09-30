import sys
sys.path.insert(0, sys.path[0] + '/models')
sys.path.insert(0, sys.path[1] + '/handlers')

from flask import Flask, render_template, request, redirect, url_for
from database import session, Category, Item

from json_cat import json_api
from newedititem import newedititem_api

app = Flask(__name__)

app.register_blueprint(json_api)
app.register_blueprint(newedititem_api)

@app.route('/')
@app.route('/index')
def Main():
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(3)
    return render_template('main.html', categories=categories, latest_items=latest_items)

@app.route('/category/new/', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        newItem = Category(name=request.form['category_name'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('Main'))
    else:
        return render_template('newcategory.html')

@app.route('/category/<int:category_id>/<int:item_id>/')
@app.route('/category/<int:category_id>/<int:item_id>/view/')
def viewItem(category_id, item_id):
    viewItem = session.query(Item).get(item_id)
    return render_template('viewitem.html', item=viewItem)

@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods=['GET','POST'])
def deleteItem(category_id, item_id):
    deleteItem = session.query(Item).get(item_id)
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        # Remove the image from the filesystem
        return redirect(url_for('ListItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=deleteItem)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/list')
def ListItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).get(category_id)
    return render_template('category.html', items=items, category=category.name)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

