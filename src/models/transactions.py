from src.db import db


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    transactionID = db.Column(
        db.String(255)
    )
    transactionRef = db.Column(
        db.String(255),
        unique=True
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
        db.DateTime
    )

    def __repr__(self):
        return "<Transaction: {}>".format(self.transactionRef)
    
    def save(self):
        """Commit model values to database"""
        
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        """ Fetch all Transactions from database"""
        
        return Transaction.query.all()
        