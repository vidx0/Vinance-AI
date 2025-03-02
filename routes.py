from flask import jsonify, render_template, redirect, session, url_for, request, flash
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

@app.route('/chatbot/respond', methods=['POST'])
def chatbot_respond():
    user_message = request.json.get("message", "")
    
    # Retrieve conversation history from session
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append({"user": user_message})

    # Placeholder AI logic
    if "budget" in user_message.lower():
        bot_response = "It looks like you're asking about your budget. What specific details do you need?"
    else:
        bot_response = "I'm here to help with budgeting! Try asking about your savings or expenses."

    session['chat_history'].append({"bot": bot_response})
    
    return jsonify({"response": bot_response, "history": session['chat_history']})
