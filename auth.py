from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from . import db
import random
import time
from .email_sender import send_email
auth = Blueprint('auth', __name__)


@auth.route('/verify_otp')
def verify_otp():
    return render_template('verify_otp.html')



@auth.route('/verify_otp', methods=['POST'])
def verify_otp_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database

    if not user or not user.password == password or int(user.time) > int(time.time()) + 1000*60*10:
        flash('Please check your otp or otp has expired ')
        return redirect(url_for('auth.verify_otp')) # if the user doesn't exist or password is wrong, reload the page


    # “Remember Me” functionality can be tricky to implement.
    # However, Flask-Login makes it nearly transparent - just pass remember=True to the login_user call.
    # A cookie will be saved on the user’s computer, and then Flask-Login will automatically restore the user ID from that cookie if it is not in the session.
    # The amount of time before the cookie expires can be set with the REMEMBER_COOKIE_DURATION configuration or it can be passed to login_user.
    # The cookie is tamper-proof, so if the user tampers with it (i.e. inserts someone else’s user ID in place of their own),
    # the cookie will merely be rejected, as if it was not there.


    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    ctime = int(time.time()) + 1000*60*10
    password = "1111" # str(random.randint(100000, 999999))  # request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    # if user: # if a user is found, we want to redirect back to signup page so user can try again
    #     flash('Email address already exists')
    #     return redirect(url_for('auth.signup'))
    send_email(email, "Your OTP is " + password + " <eom>", "")
    if user:
        user.time = ctime
        user.password = password
        db.session.commit()
        flash("OTP sent to your email")
        return redirect(url_for('auth.verify_otp'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=password, time=ctime)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.verify_otp'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


