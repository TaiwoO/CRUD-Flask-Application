from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    menu_items = db.relationship('MenuItem', backref='restaurant')

    # def __init__(self, name, menu_items):
    #     self.name = name

    def __repr__(self):
        return '<Restaurant %r>' % self.name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    # def __init__(self, id, name, course, description, price, restaurant_id):
    #     self.id = id
    #     self.name = name
    #     self.course = course
    #     self.description = description
    #     self.price = price
    #     self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<MenuItem %r>' % self.name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'course': self.course
        }


