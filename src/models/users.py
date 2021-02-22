from src.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """model representing users table."""
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = db.Column(
        db.String(100),
        unique=True
    )
    phone = db.Column(
        db.String(50),
        nullable=False
    )
    full_name = db.Column(
        db.String(100)
    )
    customer_id = db.Column(
        db.String(100)
    )
    transactions = db.relationship(
        'Transaction', 
        backref = 'user', 
        lazy = 'joined'
    )
    cards = db.relationship(
        'Card', 
        backref = 'user', 
        lazy = 'joined'
    )
    
    def __repr__(self):
        return "<User: {}>".format(self.email)
    
    
    def save(self):
        """Commit model values to database"""
        
        db.session.add(self)
        db.session.commit()