from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt, login_manager
from models import User, Transaction
import uuid
from datetime import datetime
from flask_mail import Mail, Message



from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt, login_manager
from models import User, Transaction
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route (Budget Page)
@app.route("/")
@login_required
def home():
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).all()
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    remaining = total_income - total_expense
    
    next_paycheck = current_user.get_next_paycheck()
    
    return render_template("index.html",
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        remaining=remaining,
        next_paycheck=next_paycheck
    )


@app.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")

# Stock Predictions page
@app.route("/stocks")
@login_required
def stocks():
    return render_template("stocks.html")

# Register route with email verification
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import db, User

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        flash("Invalid email or password", "danger")
    return render_template("login.html")

# Register route (simplified)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login", "success")
        return redirect(url_for("login"))

    return render_template("register.html")



# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))




