import os
import urllib

from flask import Flask, Blueprint, request, redirect, url_for
from database import session, Category, User, Item
from users_api import getCurrentUser, validUserPermission
from base import render_template
from forms import CategoryForm

category_api = Blueprint('category_api', __name__)

@category_api.route('/category/new/', methods=['GET','POST'])
def newCategory():
    if getCurrentUser() is None:
        return redirect('/login')
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(name = form.name.data,
                                user_id = getCurrentUser())
        session.add(newCategory)
        session.commit()
        return redirect(url_for('category_api.ListItems', category_id=newCategory.id))
    else:
        return render_template('newcategory.html', form=form)

@category_api.route('/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
    editCategory = session.query(Category).get(category_id)
    if not validUserPermission(editCategory.user.id):
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    form = CategoryForm(request.form, obj=editCategory)
    if request.method == 'POST' and form.validate():
        editCategory.name = form.name.data
        session.commit()
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    else:
        return render_template('editcategory.html', category=editCategory, form=form)

@category_api.route('/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id):
    deleteCategory = session.query(Category).get(category_id)
    if not validUserPermission(deleteCategory.user.id):
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    if request.method == 'POST':
        #remove all items in category.
        items = session.query(Item).filter_by(category_id=category_id)
        for x in items:
            session.delete(x)
        session.delete(deleteCategory)
        session.commit()
        # TODO remove all images
        return redirect(url_for('Main'))
    else:
        return render_template('deletecategory.html', category=deleteCategory)


@category_api.route('/category/<int:category_id>/')
@category_api.route('/category/<int:category_id>/list')
def ListItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).get(category_id)
    return render_template('category.html', items=items, category=category,
                                    usersCategory = validUserPermission(category.user.id))

