from src.db import db


class Card(db.Model):
    """model representing cards table."""
    
    __tablename__ = 'cards'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    token = db.Column(
        db.String(255),
        nullable=False
    )
    card_type = db.Column(
        db.String(100)
    )
    card_expiry = db.Column(
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
    
    def save(self):
        """Commit model values to database"""
        
        db.session.add(self)
        db.session.commit()