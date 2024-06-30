#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class RestaurantList(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in restaurants], 200

class RestaurantDetail(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {'error': 'Restaurant not found'}, 404
        restaurant_pizzas = restaurant.restaurant_pizzas
        restaurant_pizzas_data = []
        for restaurant_pizza in restaurant_pizzas:
            pizza = restaurant_pizza.pizza
            restaurant_pizzas_data.append({
                'id': restaurant_pizza.id,
                'pizza_id': restaurant_pizza.pizza_id,
                'price': restaurant_pizza.price,
                'restaurant_id': restaurant_pizza.restaurant_id,
                'pizza': {
                    'id': pizza.id,
                    'name': pizza.name,
                    'ingredients': pizza.ingredients
                }
            })
        return {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'restaurant_pizzas': restaurant_pizzas_data
        }, 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {'error': 'Restaurant not found'}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

class PizzaList(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas], 200

class RestaurantPizzaCreate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('pizza_id', type=int, required=True)
        parser.add_argument('restaurant_id', type=int, required=True)
        args = parser.parse_args()

        try:
            restaurant_pizza = RestaurantPizza(**args)
            db.session.add(restaurant_pizza)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 500

        restaurant = restaurant_pizza.restaurant
        pizza = restaurant_pizza.pizza
        response = {
            'id': restaurant_pizza.id,
            'price': restaurant_pizza.price,
            'pizza_id': restaurant_pizza.pizza_id,
            'restaurant_id': restaurant_pizza.restaurant_id,
            'pizza': {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            },
            'restaurant': {
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address
            }
        }
        return response, 201  # Return 201 status code here

api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantDetail, '/restaurants/<int:id>')
api.add_resource(PizzaList, '/pizzas')
api.add_resource(RestaurantPizzaCreate, '/restaurant_pizzas')

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

if __name__ == "__main__":
    app.run(port=5555, debug=True)
