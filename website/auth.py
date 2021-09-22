from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category="success")

                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password Try again!', category="failure")
        else:
            flash('Email doesn\'t exist', category="failure")


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category="failure")
        #Validity check for creating account
        elif len(email) <4:
            flash('Email is must be greater than 4 characters.', category='failure')

        elif len(firstName) < 2:
            flash('Please enter a valid firstName', category='failure')
        elif password1 != password2:
            flash('Please check if you entered the password correctly.', category='failure')
        elif len(password1) <4:
            flash('Password must be at least 4 characters!', category='failure')
        else:
            #add user to database
            new_user = User(email = email, first_name = firstName, password=generate_password_hash(password1, "sha256"))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    if request.method=="GET":
        pass
    return render_template("sign-up.html", user=current_user)