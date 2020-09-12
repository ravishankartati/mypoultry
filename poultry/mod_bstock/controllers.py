# Import flask dependencies
from flask import Blueprint, request, make_response, jsonify, g, session

# Import the database object from the main app module
from poultry import db
import json

# Import module models
from poultry.mod_auth.models import User
from poultry.mod_shed.models import Shed
from poultry.mod_bstock.models import Birdstock

mod_bstock = Blueprint('bstock', __name__, url_prefix='/bstock')


@mod_bstock.route('/create', methods=['POST'])
def create():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        user_id = User.decode_auth_token(auth_token)
        if not isinstance(user_id, str):
            quantity = int(request.json['quantity'])
            btype = request.json['btype']
            age = int(request.json['age'])
            shed_number = int(request.json['shed'])
            shed = Shed.query.filter_by(shed=shed_number).first()
            bstock = Birdstock.query.filter_by(
                bshed=shed_number, age=age, btype=btype).first()
            if not shed:
                return make_response(jsonify({
                    'status': 'fail',
                    'message': 'Shed number does not exists,please create one.',
                })), 400
            elif not bstock:
                new_bstock = Birdstock(shed=shed, quantity=quantity,
                                       btype=btype, age=age)
                db.session.add(new_bstock)
                db.session.commit()
                return make_response(jsonify({
                    'status': 'success',
                    'message': 'Successfully bird stock is created.',
                })), 201
            else:
                return update(bstock, btype, quantity)

        return make_response(jsonify({
            'status': 'fail',
            'message': 'user_id is not an integer {}'.format(user_id)
        })), 401
    else:
        return make_response(jsonify({
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        })), 401


@mod_bstock.route('/update', methods=['POST'])
def update(bstock, btype, quantity):
    try:
        bstock.quantity += quantity
        bstock.btype = btype
        db.session.add(bstock)
        db.session.commit()
        return make_response(jsonify({
            'status': 'success',
            'message': 'Bird stock successfully updated.',
        })), 201

    except Exception as e:
        print(e)
        return make_response(jsonify({
            'status': 'fail',
            'message': 'Bird stock did not update.'
        })), 400
