from src.db import db


class Transaction(db.Model):
    """model representing transactions table."""
    
    __tablename__ = 'transactions'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    card_id = db.Column(
        db.Integer,
        db.ForeignKey('cards.id')
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    transaction_ref = db.Column(
        db.String(255),
        unique=True
    )
    status = db.Column(
        db.String(30)
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
        