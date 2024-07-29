from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Parcel(db.Model):
    __tablename__ = 'parcels'
    id = db.Column(db.Integer, primary_key=True)
    parcel_item = db.Column(db.String(100), nullable=False)
    parcel_description = db.Column(db.String(255), nullable=False)
    parcel_weight = db.Column(db.Float, nullable=False)
    parcel_cost = db.Column(db.Float, nullable=False)
    parcel_status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    
    destination = db.relationship('Destination', backref='parcel', uselist=False)