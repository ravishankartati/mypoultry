from poultry.mod_auth.models import User
from datetime import datetime
from poultry import db


class Shed(db.Model):
    __tablename__ = 'shed_info'
    # userid as foreign key
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'auth_user.id'), nullable=False)
    # State where shed is located
    state = db.Column(db.String(128),  nullable=False)
    # District where shed is located
    district = db.Column(db.String(128),  nullable=False)
    # Village where shed is located
    village = db.Column(db.String(128),  nullable=False)
    # Shed number
    shed = db.Column(db.Integer,  primary_key=True)
    # Relationships
    bstocks = db.relationship('Birdstock', backref='shed', single_parent=True)

    # New instance instantiation procedure
    def __init__(self, user, state, district, village, shed):
        self.user = user
        self.state = state
        self.district = district
        self.village = village
        self.shed = shed
