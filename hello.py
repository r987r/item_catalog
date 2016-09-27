from flask import Flask
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

@app.route('/category/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
    return "delete item..."

@app.route('/category/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
    return "edit item..."

@app.route('/category/<int:category_id>/')
def ListItems(category_id):
    output = ''
    
    items = session.query(Item).filter_by(category_id=category_id)
    for i in items:
        output += i.name
        output += '<br>'
    return output



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

