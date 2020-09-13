
from poultry import db
from sqlalchemy.sql.schema import PrimaryKeyConstraint


class Birdstock(db.Model):
    __tablename__ = 'bird_stock'
    # Shed number
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    bshed = db.Column(db.Integer, db.ForeignKey(
        'shed_info.shed'), nullable=False)
    age = db.Column(db.Float,  nullable=False)
    btype = db.Column(db.String(128),  nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    bsales = db.relationship('Birdsales', backref='bstock', single_parent=True)    

    __table_args__ = (
        PrimaryKeyConstraint('bshed', 'age', 'btype'),
        {},
    )

    def __init__(self, shed, age, btype, quantity):
        # shed belongs to the relationship backref varuable in shed_info
        self.shed = shed
        self.age = age
        self.btype = btype
        self.quantity = quantity
