import traceback
from flask import jsonify, render_template, redirect, session, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt, login_manager
from models import User, Transaction, Debt
import uuid
from datetime import datetime
from flask_mail import Mail, Message
import joblib
import numpy as np
import pandas as pd



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



@app.route("/add_income", methods=["POST"])
@login_required
def add_income():
   try:
       amount = float(request.form.get("amount"))
       pay_frequency = request.form.get("pay_frequency")
      
       new_income = Transaction(
           user_id=current_user.id,
           type='income',
           category='Paycheck',
           amount=amount,
           date=datetime.utcnow()
       )
       current_user.salary = float(request.form.get("amount"))
       print(f"Debug: current_user.salary = {current_user.salary}")
       current_user.pay_frequency = pay_frequency
       current_user.last_paycheck_date = datetime.utcnow()
      
       db.session.add(new_income)
       db.session.commit()
       flash("Paycheck added successfully!", "success")
   except ValueError:
       flash("Invalid amount entered", "danger")
   except Exception as e:
       flash("Error adding paycheck", "danger")
  
   return redirect(url_for("home"))






# Paycheck update route
@app.route("/update_paycheck", methods=["POST"])
@login_required
def update_paycheck():
   salary = request.form.get("salary")
   pay_frequency = request.form.get("pay_frequency")


   if salary and pay_frequency:
       current_user.salary = float(salary)
       current_user.pay_frequency = pay_frequency
       current_user.last_paycheck_date = datetime.utcnow()
       db.session.commit()
       flash("Paycheck details updated!", "success")


   return redirect(url_for("home"))


@app.route("/add_expense", methods=["POST"])
@login_required
def add_expense():
   try:
       category = request.form.get("category")
       amount = float(request.form.get("amount"))
      
       new_expense = Transaction(
           user_id=current_user.id,
           type='expense',
           category=category,
           amount=amount,
           date=datetime.utcnow()
       )
      
       db.session.add(new_expense)
       db.session.commit()
       flash("Expense added successfully!", "success")
   except ValueError:
       flash("Invalid amount entered", "danger")
   except Exception as e:
       flash("Error adding expense", "danger")
  
   return redirect(url_for("home"))

import re
import pandas as pd
import joblib
from flask import request, jsonify, session
from flask_login import current_user
from models import Transaction, Debt
from app import db

# Load AI model and scaler
model = joblib.load("AI_models/budget_ai_model.pkl")
scaler = joblib.load("AI_models/scaler.pkl")
import requests


OPENROUTER_API_KEY = "key"  # Replace with your actual OpenRouter API key

@app.route('/chatbot/respond', methods=['POST'])
def chatbot_respond():
    user_message = request.json.get("message", "").lower().strip()

    if not current_user.is_authenticated:
        return jsonify({"response": "Please log in to access budgeting assistance."})

    # --- Pull financial data from the user ---
    user_income = current_user.salary or 0
    user_savings = current_user.calculate_savings()
    total_debt = db.session.query(db.func.sum(Debt.amount)).filter_by(user_id=current_user.id).scalar() or 0

    categories = {
    "housing": 0,
    "food": 0,
    "transportation": 0,
    "entertainment": 0,
    "utilities": 0,
    "healthcare": 0,
    "subscriptions": 0,
    "other": 0
    }
    transactions = Transaction.query.filter_by(user_id=current_user.id, type='expense').all()
    for t in transactions:
        category = t.category.lower().replace(" ", "_")
        if category in categories:
            categories[category] += t.amount

    # --- Format prompt for OpenRouter AI ---
    prompt = (
        f"My income is ${user_income:.2f}, my current savings are ${user_savings:.2f}, "
        f"and my total debt is ${total_debt:.2f}.\n"
        f"My expenses are as follows:\n" +
        f"You are a helpful AI budgeting assistant. Always use clear, friendly language, include real numbers when possible, and suggest financing or flexible payment options when relevant.\n" +
        "\n".join([f"- {k.replace('_', ' ').title()}: ${v:.2f}" for k, v in categories.items()]) +
        f"\n\nNow answer the question: '{user_message}'"
    )

    # --- Call OpenRouter API ---
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # Use a supported model
                "messages": [
                    {"role": "system", "content": "You are a helpful budgeting assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response_json = response.json()
        print("OpenRouter response:", response_json)

        api_reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "AI did not respond.")
    except Exception as e:
        print("Chatbot error:", e)
        print("Full response:", response.text if 'response' in locals() else 'No response received')
        api_reply = "There was an error getting a response from the AI."

    # Save the exchange to session history
    session.setdefault('chat_history', []).append({"user": user_message, "bot": api_reply})
    return jsonify({"response": api_reply, "history": session['chat_history']})

from AI_models.train_stock_model import train_stock_model
from AI_models.predict_stock import predict_stock


@app.route('/train', methods=['POST'])
def train():
    """Train the stock prediction model for a given stock."""
    data = request.get_json()
    stock_symbol = data.get('stock_symbol', '').upper()

    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        train_stock_model(stock_symbol)
        return jsonify({"message": f"Model for {stock_symbol} trained successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Predict the next day's closing price for a given stock."""
    data = request.get_json()
    stock_symbol = data.get('stock_symbol', '').upper()

    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        predicted_price = predict_stock(stock_symbol)

        if predicted_price is None:
            app.logger.error(f"Prediction failed for {stock_symbol}")
            return jsonify({"error": "Prediction failed"}), 500

        return jsonify({"stock_symbol": stock_symbol, "predicted_price": float(predicted_price)})
    
    except Exception as e:
        error_message = traceback.format_exc()  # Get full error details
        app.logger.error(f"Prediction failed for {stock_symbol}: {error_message}")
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500  # Return error details

