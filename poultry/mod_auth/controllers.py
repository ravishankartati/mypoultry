# Import flask dependencies

from flask import Blueprint, request, make_response, jsonify, g, session
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from poultry import db
import json

# Import module models (i.e. User)
from poultry.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signup', methods=['POST'])
def signup():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    role = request.json['role']
    status = request.json['status']
    user = User.query.filter_by(email=email).first()
    if not user:
        try:
            new_user = User(email=email, phone=phone, name=name, status=status, role=role, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token(new_user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
           
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


@mod_auth.route('/signin', methods=['POST'])
def signin():
    try:
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500
