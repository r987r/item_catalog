from wtforms import Form, StringField, TextAreaField, validators

class CategoryForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])

class ItemForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    description = TextAreaField('description', [validators.Length(min=10)])

class ItemNewForm(ItemForm):
    img_url = StringField('img_url', [validators.url(require_tld=True)])

class ItemEditForm(ItemForm):
    img_url = StringField('img_url', [validators.Optional(), validators.url(require_tld=True)])
