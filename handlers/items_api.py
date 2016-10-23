import os
import urllib

from flask import Flask, Blueprint, request, redirect, url_for
from database import session, Item, User, Category
from users_api import validUserPermission
from base import render_template
from forms import ItemNewForm, ItemEditForm


items_api = Blueprint('items_api', __name__)

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

@items_api.route('/category/<int:category_id>/new/', methods=['GET','POST'])
def newItem(category_id):
    category = session.query(Category).get(category_id)
    if not validUserPermission(category.user.id):
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    form = ItemNewForm(request.form)
    if request.method == 'POST' and form.validate():
        newItem = Item(name = form.item_name.data,
                        description = form.description.data,
                        img_url = "",
                        category_id=category_id)
        session.add(newItem)
        session.flush() # Needed to get id for the new item.
        newItem.img_url = handleImage(form.img_url.data, category_id, newItem.id)
        session.commit()
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    else:
        return render_template('newitem.html', category=category, form=form)

@items_api.route('/category/<int:category_id>/<int:item_id>/edit/', methods=['GET','POST'])
def editItem(category_id, item_id):
    editItem = session.query(Item).get(item_id)
    if not validUserPermission(editItem.category.user.id):
        return redirect(url_for('items_api.viewItem', category_id=category_id, item_id=item_id))
    form = ItemEditForm(request.form, obj=editItem)
    if request.method == 'POST' and form.validate():
        editItem.name = form.name.data
        editItem.description = form.description.data
        img_url = form.img_url.data
        if(img_url != ""):
           editItem.img_url = handleImage(img_url, category_id, item_id)
        session.commit()
        return redirect(url_for('items_api.viewItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('edititem.html', item=editItem, form=form)

@items_api.route('/category/<int:category_id>/<int:item_id>/')
@items_api.route('/category/<int:category_id>/<int:item_id>/view/')
def viewItem(category_id, item_id):
    viewItem = session.query(Item).get(item_id)
    return render_template('viewitem.html', item=viewItem,
                            usersItem = validUserPermission(viewItem.category.user.id))



@items_api.route('/category/<int:category_id>/<int:item_id>/delete/', methods=['GET','POST'])
def deleteItem(category_id, item_id):
    deleteItem = session.query(Item).get(item_id)
    if not validUserPermission(deleteItem.category.user.id):
        return redirect(url_for('items_api.viewItem', category_id=category_id, item_id=item_id))
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        # Remove the image from the filesystem
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=deleteItem)



