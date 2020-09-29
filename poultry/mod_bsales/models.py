from poultry import db
from sqlalchemy.sql.schema import PrimaryKeyConstraint


class Birdsales(db.Model):
    __tablename__ = 'bird_sales'
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    age = db.Column(db.Float,  nullable=False)
    btype = db.Column(db.String(128),  nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    bshed = db.Column(db.Integer, db.ForeignKey(
        'bird_stock.bshed'), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('bshed', 'age', 'btype', 'quantity', 'amount'),
        {},
    )

    def __init__(self, age, btype, quantity, amount, bstock):
        # bstock belongs to the relationship backref varuable in bird_stock table
        self.bstock = bstock
        self.age = age
        self.btype = btype
        self.quantity = quantity
        self.amount = amount
