from flask import Blueprint, render_template, flash, request, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import Feedback
import time
from time import strftime, localtime
from email_sender import send_email
# this is basically create component in the application, that can imported along with all its routes, etc.
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return redirect(url_for('main.profile'))

# what is happen if not loggedin , it will redirect to - login_manager.login_view = 'auth.login'
# It will flash a message "Please log in to access this page" on top of lgoin page.
# we can change this message and check other configs in flash_login.config file.
# question how to override the configs.

@main.route('/profile')
@login_required
def profile():
    feedbacks = Feedback.query.filter_by(email=current_user.email).all()
    print("feedbacks ", feedbacks)
    feedbacks = [{"time": strftime('%Y-%m-%d %H:%M:%S', localtime(feedback.time)), "bad": feedback.bad, "good": feedback.good} for feedback in feedbacks]
    return render_template('profile.html', name=current_user.name, feedbacks=feedbacks)

@main.route("/send_feedback")
@login_required
def send_feedback():
    return render_template('sendfeedback.html')

@main.route("/send_feedback", methods=['POST'])
@login_required
def send_feedback_post():
    email = request.form.get('email')
    good = request.form.get('good')
    bad = request.form.get('bad')
    name = request.form.get("name")
    new_feedback = Feedback(email=email, from_email=current_user.email, good=good, bad=bad, time=int(time.time()))
    # add the new user to the database
    db.session.add(new_feedback)
    db.session.commit()
    body = f'<pre>Dear {name},' \
           f'\n\nWe hope you\'re doing well!' \
           f'\n\nWe wanted to let you know that you\'ve received new feedback on our platform. ' \
           f'To view the message, simply click the link below:' \
           f'\n\n<a href="http://192.168.0.134:8080/profile">View Feedback</a>' \
           f'\n\nFeel free to check it out at your convenience. ' \
           f'If you have any questions or need assistance, please don\'t hesitate to reach out.' \
           f'\n\nBest regards,' \
           f'\nThe Totokoko Team</pre>'
    send_email(email, "You've Received New Feedback", body)
    flash(f"feedback send to {email}")
    return render_template('sendfeedback.html')

