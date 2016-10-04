import os
import urllib

from flask import Flask, Blueprint, render_template, request, redirect, url_for
from database import session, Category, Item

category_api = Blueprint('category_api', __name__)

@category_api.route('/category/new/', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['category_name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('Main'))
    else:
        return render_template('newcategory.html')

@category_api.route('/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
    editCategory = session.query(Category).get(category_id)
    if request.method == 'POST':
        editCategory.name = request.form['category_name']
        session.commit()
        return redirect(url_for('category_api.ListItems', category_id=category_id))
    else:
        return render_template('editcategory.html', category=editCategory)

@category_api.route('/category/<int:category_id>/')
@category_api.route('/category/<int:category_id>/list')
def ListItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    category = session.query(Category).get(category_id)
    return render_template('category.html', items=items, category=category.name)


