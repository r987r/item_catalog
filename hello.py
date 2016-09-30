from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entries import Base, Category, Item

import os
import urllib

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/category/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])

@app.route('/category/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(CategoryItems=[i.serialize for i in items])

@app.route('/category/<int:category_id>/<int:item_id>/JSON/')
def itemsJSON(category_id, item_id):
    viewItem = session.query(Item).get(item_id)
    return jsonify(item=viewItem.serialize)


@app.route('/')
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

def handleImage(public_url, category_id, item_id):
    # Handle storing images on server and return path on server to caller.
    # TODO: Throw an error when bad image is seen (url or size)
    extension = os.path.splitext(public_url)[1]
    save_path = "./static/images/c%d" % category_id
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    save_path = "%s/i%d" % (save_path, item_id)
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    for the_file in os.listdir(save_path):
        # Remove any files in this directory incase of an edit.
        file_path = os.path.join(save_path, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    save_path = "images/c%d/i%d/img%s" % (category_id, item_id, extension)
    urllib.urlretrieve(public_url, "./static/" + save_path)
    return save_path

@app.route('/category/<int:category_id>/new/', methods=['GET','POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['item_name'],
                        description= request.form['description'],
                        img_url = "",
                        category_id=category_id)
        session.add(newItem)
        session.flush() # Needed to get id for the new item.
        newItem.img_url = handleImage(request.form['img_url'], category_id, newItem.id)
        session.commit()
        return redirect(url_for('ListItems', category_id=category_id))
    else:
        return render_template('newedititem.html')

@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET','POST'])
def editItem(category_id, item_id):
    editItem = session.query(Item).get(item_id)
    if request.method == 'POST':
        editItem.name = request.form['item_name']
        editItem.description = request.form['description']
        img_url = request.form['img_url']
        if(img_url != ""):
           editItem.img_url = handleImage(img_url, category_id, item_id)
        session.commit()
        return redirect(url_for('ListItems', category_id=category_id))
    else:
        return render_template('edititem.html', item=editItem)


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


@app.route('/category/<int:category_id>/list')
def ListItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).get(category_id)
    return render_template('category.html', items=items, category=category.name)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

