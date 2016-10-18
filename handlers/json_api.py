from flask import Blueprint, jsonify
from database import session, Category, Item
from sqlalchemy.orm import sessionmaker
import json

json_api = Blueprint('json_api', __name__)


@json_api.route('/category/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])

@json_api.route('/category/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(CategoryItems=[i.serialize for i in items])

@json_api.route('/category/<int:category_id>/<int:item_id>/JSON/')
def itemsJSON(category_id, item_id):
    viewItem = session.query(Item).get(item_id)
    return jsonify(item=viewItem.serialize)

