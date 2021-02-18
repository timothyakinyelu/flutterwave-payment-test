from src.db import db


class Card(db.Model):
    __tablename__ = 'cards'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    token = db.Column(
        db.String(255)
        nullable=False
    )
    card_type = db.Column(
        db.String(100)
    )
    card_expiry = db.Column(
        db.String(100)
    )
    first_six_digits = db.Column(
        db.String(100)
    )
    last_four_digits = db.Column(
        db.String(100)
    )
    country = db.Column(
        db.String(100)
    )
    transactions = db.relationship(
        'Transaction',
        backref = 'card',
        lazy = 'joined'
    )