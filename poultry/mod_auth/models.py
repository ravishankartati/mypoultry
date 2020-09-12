# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from poultry import db, app
import jwt
from datetime import datetime, timedelta

# Define a User model
class User(db.Model):

    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False,
                      unique=True)
    password = db.Column(db.String(192),  nullable=False)
    phone = db.Column(db.String(128),  nullable=False)

    # Authorisation Data: role & status
    role = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)

    sheds = db.relationship('Shed',
                      backref='user',
                      cascade='all, delete, delete-orphan',
                      single_parent=True)

    # New instance instantiation procedure
    def __init__(self, name, email, password, phone, role, status):

        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role
        self.status = status

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=5),
                'iat': datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
