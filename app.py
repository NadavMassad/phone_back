import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Phones(db.Model):
    id = db.Column('animal_id', db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    color = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __init__(self, brand, color, price):
        self.brand = brand
        self.color = color
        self.price = price


@app.route('/phones/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/phones/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def crud_phone(id=-1):
    if request.method == 'GET':
        res = []
        for phone in Phones.query.all():
            res.append({'id': phone.id, 'brand': phone.brand,
                       'color': phone.color, 'price': phone.price})
        return (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        brand = request_data['brand']
        color = request_data['color']
        price = request_data['price']
        new_phone = Phones(brand, color, price)
        db.session.add(new_phone)
        db.session.commit()
        return 'New Phone Was Added'
    if request.method == 'DELETE':
        del_phone = Phones.query.get(id)
        db.session.delete(del_phone)
        db.session.commit()
        return 'A Phone Was Deleted'
    if request.method == 'PUT':
        update_phone = Phones.query.get(id)
        brand = request.json['brand']
        color = request.json['color']
        price = request.json['price']
        update_phone.brand = brand
        update_phone.color = color
        update_phone.price = price
        db.session.commit()
        return 'A Phone Was Edited'


@app.route('/')
def test():
    return 'Test'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
