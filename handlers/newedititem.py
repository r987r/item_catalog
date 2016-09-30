import os
import urllib

from flask import Flask, Blueprint, render_template, request, redirect, url_for
from database import session, Item

newedititem_api = Blueprint('newedititem_api', __name__)

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

@newedititem_api.route('/category/<int:category_id>/new/', methods=['GET','POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['item_name'],
                        description= request.form['description'],
                        img_url = "",
                        category_id=category_id)
        session.new(newItem)
        session.flush() # Needed to get id for the new item.
        newItem.img_url = handleImage(request.form['img_url'], category_id, newItem.id)
        session.commit()
        return redirect(url_for('ListItems', category_id=category_id))
    else:
        return render_template('newitem.html')

@newedititem_api.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET','POST'])
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

