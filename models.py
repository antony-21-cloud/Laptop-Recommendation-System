from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Float

db = SQLAlchemy()

# 1. THE USER MODEL (The Security Guard)
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='student') # student, seller, admin
    
    # Specific for Students
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=True)
    
    # Relationship: A Seller (User) owns many laptops
    laptops = relationship("Laptop", back_populates="seller")

# 2. THE COURSE MODEL (The Expert Rules)
class Course(db.Model):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    min_ram: Mapped[int] = mapped_column(Integer)
    min_cpu_score: Mapped[int] = mapped_column(Integer)

# 3. THE LAPTOP MODEL (The Warehouse Item)
class Laptop(db.Model):
    __tablename__ = "laptops"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    ram: Mapped[int] = mapped_column(Integer)
    cpu_score: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    
    # The Handshake: Links Laptop to a Seller (User)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    seller = relationship("User", back_populates="laptops")