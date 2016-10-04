from flask import render_template as render_template_flask
from database import session, Category
from users_api import getCurrentUser, validUserPermission

def render_template(page, **kw):
    kw["categories"] = session.query(Category).all()
    kw["loggedIn"] = getCurrentUser is not None
    return render_template_flask(page,**kw)
    
