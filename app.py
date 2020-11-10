from os import uname
import sqlite3
from flask import Flask, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# db configs
db_path = os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init DB
db = SQLAlchemy(app)
# init MA
ma = Marshmallow(app)

# Models


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity ')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'Hello world'})

# add item
@app.route('/item', methods=['POST'])
def add_item():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_item = Item(name, description, price, quantity)
    db.session.add(new_item)
    db.session.commit()

    return product_schema.jsonify(new_item)

# get all items
@app.route('/item', methods=['GET'])
def get_products():
    all_items = Item.query.all()
    result = products_schema.dump(all_items)
    return jsonify(result)

# get single item
@app.route('/item/<id>', methods=['GET'])
def get_product(id):
    item = Item.query.get(id)
    return product_schema.jsonify(item)

# update an item
@app.route('/item/<id>', methods=['PUT'])
def add_product(id):
    item = Item.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    item.name = name
    item.description = description
    item.price = price
    item.qty = quantity

    db.session.commit()
    return product_schema.jsonify(item)

# delete item
@app.route('/item/<id>', methods=['DELETE'])
def delete_product(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return product_schema.jsonify(item)


# start server
if __name__ == '__main__':
    app.run(debug=True)
    print("Hello")
