from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entries import Base, Category, Item
app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def HelloWorld():
    categories = session.query(Category).all()
    output = ''
    for category in categories:
        output += category.name + " " + str(category.id)
    return output

@app.route('/category/<int:category_id>/new/')
def newItem(category_id):
    return "new item..."

@app.route('/category/<int:category_id>/<int:item_id>/view/')
def viewItem(category_id, item_id):
    return "view item..."

@app.route('/category/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
    return "delete item..."

@app.route('/category/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
    return "edit item..."

@app.route('/category/<int:category_id>/')
def ListItems(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('category.html', items=items)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

