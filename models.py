from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    pay_frequency = db.Column(db.String(50), nullable=True)
    last_paycheck_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_next_paycheck(self):
        if not self.last_paycheck_date or not self.pay_frequency:
            return None
        if self.pay_frequency == "weekly":
            return self.last_paycheck_date + timedelta(weeks=1)
        elif self.pay_frequency == "biweekly":
            return self.last_paycheck_date + timedelta(weeks=2)
        elif self.pay_frequency == "monthly":
            return self.last_paycheck_date + timedelta(weeks=4)
        return None

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)