from src.db import db


card_user_table = db.Table('card_user', db.Model.metadata,
    db.Column(
        'card_id', 
        db.Integer, 
        db.ForeignKey('cards.id')
    ),
    db.Column(
        'user_id', 
        db.Integer, 
        db.ForeignKey('users.id')
    )           
)