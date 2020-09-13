# Import flask dependencies
from flask import Blueprint, request, make_response, jsonify, g, session

# Import the database object from the main app module
from poultry import db
import json

# Import module models
from poultry.mod_bstock.models import Birdstock
from poultry.mod_auth.models import User
from poultry.mod_bsales.models import Birdsales

mod_bsales = Blueprint('bsales', __name__, url_prefix='/bsales')


@mod_bsales.route('/create', methods=['POST'])
def create():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        user_id = User.decode_auth_token(auth_token)
        if not isinstance(user_id, str):
            try:
                age = float(request.json['age'])
                quantity = float(request.json['quantity'])
                btype = request.json['btype']
                amount = float(request.json['amount'])
                shed_number = int(request.json['shed'])
                bstock = Birdstock.query.filter_by(bshed=shed_number).first()
                bsales = Birdsales.query.filter_by(bshed=shed_number, age=age, btype=btype).first()
                if not bstock:
                    return make_response(jsonify({
                        'status': 'fail',
                        'message': 'No stock in that shed.',
                    })), 200
                elif not bsales:
                    new_bsales = Birdsales(age=age, quantity=quantity, amount=amount,
                                           btype=btype, bstock=bstock)
                    db.session.add(new_bsales)
                    db.session.commit()
                    return make_response(jsonify({
                        'status': 'success',
                        'message': 'Successfully bsales created.',
                    })), 201
                else:
                    return update(bsales, quantity, amount)
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    'status': 'fail',
                    'message': 'Try again db error'
                })), 400
        return make_response(jsonify({
            'status': 'fail',
            'message': user_id
        })), 401
    else:
        return make_response(jsonify({
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        })), 401


@mod_bsales.route('/update', methods=['POST'])
def update(bsales, quantity, amount):
    try:
        bsales.quantity += quantity
        bsales.amount += amount
        db.session.add(bsales)
        db.session.commit()
        return make_response(jsonify({
            'status': 'success',
            'message': 'Bird sales successfully updated.',
        })), 201

    except Exception as e:
        print(e)
        return make_response(jsonify({
            'status': 'fail',
            'message': 'Bird sales did not update.'
        })), 400
