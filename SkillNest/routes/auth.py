from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


# 📝 Register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        location = request.form['location']

        # check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(
            name=name,
            email=email,
            password=password,
            location=location
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# 🔑 Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", "danger")
            return render_template('login.html')  # ✅ IMPORTANT

    return render_template('login.html')  # ✅ ALWAYS RETURN

# 🚪 Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')