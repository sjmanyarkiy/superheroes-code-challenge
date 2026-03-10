#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes')
def get_heroes():

    heroes = Hero.query.all()
    
    body = [hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes]


    return make_response(body, 200)

@app.route('/heroes/<int:id>')
def get_hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    if hero:
        body = hero.to_dict()
        status = 200
    else:
        body = {'error' : 'Hero not found'}
        status = 404

    return make_response(body, status)

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    
    body = [power.to_dict() for power in powers]


    return make_response(body, 200)

# @app.route('/powers/<int:id>')
# def get_powers_by_id(id):
#     power = Power.query.filter(Power.id == id).first()

#     if power:
#         body = power.to_dict()
#         status = 200
#     else:
#         body = {'error' : 'Power not found'}
#         status = 404

#     return make_response(body, status)

@app.route('/powers/<int:id>', methods = ['GET', 'PATCH'])
def update_powers(id):
    power = Power.query.filter(Power.id == id).first()

    if power is None:
        response_body = {'error': 'Power not found'}
        return make_response(response_body, 404)

    if request.method == 'GET':
        power_dict = power.to_dict()
        response = make_response(power_dict, 200)
        return response

    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            for attr in data:
                setattr(power, attr, data[attr])

            db.session.add(power)
            db.session.commit()

            response = make_response(power.to_dict(), 200)
            return response

        except ValueError as e:
            return make_response({'errors': [str(e)]}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
