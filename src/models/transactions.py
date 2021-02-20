from src.db import db


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    transactionID = db.Column(
        db.String(255),
        nullable=False
    )
    transactionRef = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    card_id = db.Column(
        db.Integer,
        db.ForeignKey('cards.id')
    )
    donation_type = db.Column(
        db.String(30)
    )
    currency = db.Column(
        db.String(12),
        nullable=False
    )
    payment_type=db.Column(
        db.String(30),
        nullable=False
    )
    amount = db.Column(
        db.Float
    )
    created_at = db.Column(
        db.String(255)
    )

    def __repr__(self):
        return "<Transaction: {}>".format(self.transactionRef)