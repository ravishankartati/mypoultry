# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from poultry import db, app
import jwt
from datetime import datetime, timedelta


class Permission:
    Read = 0x01
    Write = 0x02
    ReadWrite = 0x03


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Incharge': (Permission.Write, True),
            'Manager': (Permission.Read |
                        Permission.Write, False),
            'Owner': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
                db.session.commit()


# Define a User model
class User(db.Model):
    __tablename__ = 'auth_user'
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False,
                      unique=True)
    phone = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(192),  nullable=False)
    role_id = db.Column(db.String(50), db.ForeignKey(
        'role.id'), nullable=False)

    # Relationships
    sheds = db.relationship('Shed',
                            backref='user',
                            cascade='all, delete, delete-orphan',
                            single_parent=True)

    # New instance instantiation procedure

    def __init__(self, name, email, phone, password):

        self.name = name
        self.email = email
        self.phone = phone 
        self.password = password

        if self.role is None:
            if self.email == app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            elif self.role is None:
                self.role = Role.query.filter_by(default=False,).first()
                print(self.role.name)

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
            print(app.config.get('SECRET_KEY'))
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
