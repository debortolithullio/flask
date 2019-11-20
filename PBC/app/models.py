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
        return '<Item {}/{} - ${}>'.format(self.category, self.title, str(self.amount))

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), index=True, unique=True)
    category = db.Column(db.String(140), index=True)

    def __repr__(self):
        return '<Investment {}/{}>'.format(self.title, self.category)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    investment = db.Column(db.Integer, db.ForeignKey('investment.id'))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    net_amount = db.Column(db.Float)
    gross_amount = db.Column(db.Float)

    def __repr__(self):
        return '<Investment {}/{} - Net: ${}>'.format(str(self.investment), str(self.date), str(self.net_amount))

class InvestmentGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, index=True, unique=True)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Goal {} - Amount: ${}>'.format(str(self.year), str(self.amount))