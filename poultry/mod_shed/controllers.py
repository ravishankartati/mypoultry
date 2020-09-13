# Import flask dependencies
from flask import Blueprint, request, make_response, jsonify, g, session

# Import the database object from the main app module
from poultry import db
import json

# Import module models
from poultry.mod_shed.models import Shed
from poultry.mod_auth.models import User

mod_shed = Blueprint('shed', __name__, url_prefix='/shed')


@mod_shed.route('/create', methods=['POST'])
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
                state = request.json['state']
                district = request.json['district']
                village = request.json['village']
                shed_number = int(request.json['shed'])
                shed = Shed.query.filter_by(shed=shed_number).first()
                user = User.query.filter_by(id=user_id).first()
                if not shed:
                    new_shed = Shed(state=state, district=district,
                                    village=village, shed=shed_number, user=user)
                    db.session.add(new_shed)
                    db.session.commit()
                    return make_response(jsonify({
                        'status': 'success',
                        'message': 'Successfully shed is created.',
                    })), 201
                else:
                    return make_response(jsonify({
                        'status': 'fail',
                        'message': 'Shed already exists.',
                    })), 202
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
