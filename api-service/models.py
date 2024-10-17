""" models.py file"""
 
# SQLAlchemy Instance Is Imported
from database import db
 
# Declaring Model
class Positions(db.Model):
    __tablename__ = "positions"
 
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.REAL, nullable=False, default=0)
    y = db.Column(db.REAL,  nullable=False, default=0)
    z = db.Column(db.REAL,  nullable=False, default=0)
    sqltime = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())


def get_position(id):
    return Positions.query.filter_by(id=id).first()