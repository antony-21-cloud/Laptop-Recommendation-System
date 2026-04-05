from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user' # We go back to singular to match your error
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='student')
    
    # Profile fields
    shop_name = db.Column(db.String(150), default="My Laptop Shop")
    phone_number = db.Column(db.String(20), default="+254 700 000 000")
    address = db.Column(db.String(250), default="Nairobi, Kenya")
    bio = db.Column(db.Text, default="Professional laptop seller.")
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_ram = db.Column(db.Integer)
    min_cpu_score = db.Column(db.Integer)

class Laptop(db.Model):
    __tablename__ = 'laptops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    processor = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    
    # We point strictly to 'user.id'
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Explicitly tell SQLAlchemy how to join
    seller = db.relationship('User', backref='laptops', foreign_keys=[seller_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

class SupportTicket(db.Model):
    __tablename__ = "support_tickets"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")

class PurchaseRequest(db.Model):
    __tablename__ = 'purchase_requests'
    id = db.Column(db.Integer, primary_key=True)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptops.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')