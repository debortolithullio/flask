from datetime import datetime
from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140))
    mtype = db.Column(db.String(30))
    category = db.Column(db.String(140), index=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Item {}/{} - {}>'.format(self.category, self.title, str(self.amount))