from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import Mapped

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add these new fields:
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    field_of_study = db.Column(db.String(200), nullable=True)
    institution = db.Column(db.String(200), nullable=True)
    preferred_brands = db.Column(db.String(500), nullable=True)
    preferred_specs = db.Column(db.String(500), nullable=True)
    purpose = db.Column(db.String(500), nullable=True)

    # Seller-specific fields
    business_name = db.Column(db.String(200), nullable=True)
    registration_number = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    warranty_info = db.Column(db.String(500), nullable=True)
    payment_methods = db.Column(db.String(500), nullable=True)

    def __init__(self, username, password, role='student'):
        self.username = username
        self.password = password
        self.role = role


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

class Laptop(db.Model):
    __tablename__ = 'laptop'  # <--- Add this line
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    price: Mapped[float] = db.Column(db.Float, nullable=False)
    specs: Mapped[str] = db.Column(db.Text, nullable=False)
    processor_type: Mapped[str] = db.Column(db.String(50), nullable=False) 
    seller_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ram = db.Column(db.Integer)   # Optional RAM field    
    
    # Additional fields
    ram = db.Column(db.Integer, nullable=True)
    storage = db.Column(db.String(50), nullable=True)
    gpu = db.Column(db.String(100), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    stock_status = db.Column(db.String(20), default='in-stock')
    image = db.Column(db.Text, nullable=True)  # Store base64 image

    # This creates the link between Laptop and User
    seller = db.relationship('User', backref='laptops', foreign_keys=[seller_id])

    def __init__(self, name, price, specs, processor_type, seller_id):
        self.name = name
        self.price = price
        self.specs = specs
        self.processor_type = processor_type
        self.seller_id = seller_id
    
    # Explicitly tell SQLAlchemy how to join
    seller = db.relationship('User', backref='laptops', foreign_keys=[seller_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

class SupportTicket(db.Model):
    __tablename__ = 'support_ticket'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')

    # ADD THIS CONSTRUCTOR:
    def __init__(self, user_id, subject, message):
        self.user_id = user_id
        self.subject = subject
        self.message = message

class PurchaseRequest(db.Model):
    __tablename__ = 'purchase_request'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptop.id'), nullable=False)
    seller= db.relationship('User', backref='purchase_requests', foreign_keys=[student_id])
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    message = db.Column(db.Text, nullable=True)  # Add this
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add this
    seller_reply = db.Column(db.Text, nullable=True)
    replied_at = db.Column(db.DateTime, nullable=True)
    reply_status = db.Column(db.String(20), default='pending')  # pending, replied, read

    def __init__(self, student_id, laptop_id, seller_id, status='Pending', message=None):
        self.student_id = student_id
        self.laptop_id = laptop_id
        self.seller_id = seller_id
        self.status = status
        self.message = message