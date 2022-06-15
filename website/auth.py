from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
from . import db
from flask_login import login_user, login_required, current_user, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(f'password is incorrect', category='error')
        else:
            flash('User doesn\'t Exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        p = request.form
        email = p.get('email')
        firstname = p.get('firstname')
        password = p.get('password')
        password2 = p.get('checkpass')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 Characters', category='error')
        elif len(firstname) < 2:
            flash('Firstname must be greater than 2 Characters', category='error')
        elif password != password2:
            flash('Password are donot match', category='error')
        elif len(password) < 5 :
            flash('Password is less then 5 characters', category='error')
        else:
            NewUser = User(email=email, firstname=firstname, password=generate_password_hash(password, method='sha256'))
            db.session.add(NewUser)
            db.session.commit()
            login_user(user, remember=True)

            flash('Account Created!!!!', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)