import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
project_root = os.path.dirname(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_root, 'el_test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '57e19ea558d4967a552d03deece34a70'
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Category  {self.id} {self.name}>'


class Pairs(db.Model):
    __tablename__ = 'pairs'

    product_id = db.Column(db.Integer, db.ForeignKey(Products.id), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Categories.id), primary_key=True)

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    def __repr__(self):
        return f'<{self.product_id} - {self.category_id}>'


@app.route('/products', methods=['GET'])
def get_products_with_categories():
    result = db.session.query(Products, Pairs, Categories)\
        .select_from(Products)\
        .outerjoin(Pairs, Products.id == Pairs.product_id) \
        .outerjoin(Categories, Categories.id == Pairs.category_id) \
        .all()
    result_list = []
    for product, pair, category in result:
        if category:
            item = f'{product.name} - {category.name}'
        else:
            item = f'{product.name} - '
        print(item)
        result_list.append(item)
    return json.dumps(result_list)


@app.route('/categories', methods=['GET'])
def get_categories_with_products():
    result = db.session.query(Categories, Pairs, Products)\
        .select_from(Categories)\
        .outerjoin(Pairs, Categories.id == Pairs.category_id) \
        .outerjoin(Products, Products.id == Pairs.product_id) \
        .all()
    result_list = []
    for category, pair, product in result:
        if product:
            item = f'{category.name} - {product.name}'
        else:
            item = f'{category.name} - '
        result_list.append(item)
    return json.dumps(result_list)


@app.route('/pairs', methods=['GET'])
def get_pairs():
    result = db.session.query(Pairs, Products, Categories)\
        .select_from(Pairs)\
        .outerjoin(Products, Pairs.product_id == Products.id)\
        .outerjoin(Categories, Pairs.category_id == Categories.id)\
        .all()
    result_list = []
    for pair, product, category in result:
        item = f'{product.name} - {category.name}'
        result_list.append(item)
    return json.dumps(result_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    db.create_all()
