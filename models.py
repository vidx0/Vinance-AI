from datetime import datetime, timedelta
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    salary = db.Column(db.Float, nullable=True)  
    pay_frequency = db.Column(db.String(50), nullable=True)
    last_paycheck_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_next_paycheck(self):
        """Calculate next paycheck date based on pay frequency."""
        if not self.last_paycheck_date or not self.pay_frequency:
            return None
        pay_intervals = {"weekly": 7, "biweekly": 14, "monthly": 30}
        days = pay_intervals.get(self.pay_frequency, 0)
        return self.last_paycheck_date + timedelta(days=days) if days else None

    def calculate_savings(self):
        """Calculate net savings = Total income - Total expenses."""
        total_income = db.session.query(db.func.sum(Transaction.amount))\
            .filter_by(user_id=self.id, type='income').scalar() or 0
        total_expenses = db.session.query(db.func.sum(Transaction.amount))\
            .filter_by(user_id=self.id, type='expense').scalar() or 0
        return total_income - total_expenses


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creditor = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
