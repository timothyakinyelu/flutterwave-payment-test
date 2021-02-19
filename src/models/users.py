from src.db import db
from .pivot import card_user_table

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    ),
    customerID = db.Column(
        db.String(100),
        nullable=False
    )
    cards = db.relationship(
        'Card', 
        secondary = card_user_table, 
        backref = 'users', 
        lazy = 'joined'
    )
    
    def __repr__(self):
        return "<User: {}>".format(self.email)