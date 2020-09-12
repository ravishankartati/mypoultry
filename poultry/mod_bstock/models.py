
from poultry import db
from datetime import datetime
from sqlalchemy.sql.schema import PrimaryKeyConstraint


class Birdstock(db.Model):
    __tablename__ = 'bird_stock'
    # Shed number
    bshed = db.Column(db.Integer, db.ForeignKey(
        'shed_info.shed'), nullable=False)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    # State where shed is located
    age = db.Column(db.Integer,  nullable=False)
    btype = db.Column(db.String(128),  nullable=False)
    # District where shed is located
    # Village where shed is located
    quantity = db.Column(db.Integer,  nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('bshed', 'age', 'btype'),
        {},
    )
    # New instance instantiation procedure

    def __init__(self, shed, age, btype, quantity):
        # shed belongs to the relationship backref varuable in shed_info
        self.shed = shed
        self.age = age
        self.btype = btype
        self.quantity = quantity
