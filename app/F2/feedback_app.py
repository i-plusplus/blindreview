from flask import Flask, request, url_for, redirect, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import random
from email_sender import send_email
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'paras.sde@gmail.com'  # Change as needed
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Secure this properly
app.secret_key = 'your_secret_key'

# Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'register'

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Dummy database for users (in real applications, use a real database)
users_db = {}

# Load user function
@login_manager.user_loader
def load_user(user_id):
    user =  users_db.get(user_id)
    print('user_id', user_id, user)
    return user

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(7), nullable=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected
    reply = db.Column(db.Text, nullable=True)

# Authentication decorator
def authenticate_request():
    api_key = request.headers.get('Authorization')
    if not api_key or api_key != 'your-secure-api-key':
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/')
def home():
    return render_template('feedback_app.html')

@app.route('/verify_otp')
def verify_otp():
    return render_template('verify-otp.html')

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    email = 'masterofmasters22@gmail.com'
    print(data)
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    otp = str(random.randint(1000000, 9999999))
    otp='12'
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(email=email, otp=otp)
        db.session.add(user)
    else:
        user.otp = otp

    db.session.commit()

    # Send OTP via email
    email_status = send_email(otp, email)

    return jsonify({'status': email_status}), 200

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    print(request)
    print(data)
    email = data.get('email')
    otp = data.get('otp')
    otp = '12'
    email = 'masterofmasters22@gmail.com'
    print(data)
    user = User.query.filter_by(email=email, otp=otp).first()
    print('user', user)
    if not user:
        return jsonify({'error': 'Invalid OTP', 'status': 'No'}), 200

    user.otp = None
    db.session.commit()
    login_user(user)
    return jsonify({'status': 'Yes'}), 200
    #return redirect(url_for('profile'))


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#
#     if not email:
#         return jsonify({'error': 'Email is required'}), 400
#
#     otp = str(random.randint(1000000, 9999999))
#     user = User.query.filter_by(email=email).first()
#
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
#
#     user.otp = otp
#     db.session.commit()
#
#     # Send OTP via email
#     msg = Message('Login OTP', sender='paras.sde@gmail.com', recipients=[email])
#     msg.body = f'Your OTP is {otp}'
#     mail.send(msg)
#
#     return jsonify({'message': 'OTP sent to your email'}), 200

@app.route('/send_feedback', methods=['POST'])
@login_required
def send_feedback():
    if not current_user.is_authenticated:
        return redirect(url_for("register"))
    data = request.get_json()
    sender_id = data.get('sender_id')
    recipient_email = data.get('recipient_email')
    content = data.get('content')

    feedback = Feedback(sender_id=sender_id, recipient_email=recipient_email, content=content)
    db.session.add(feedback)
    db.session.commit()
    # send email to user
    return jsonify({'message': 'Feedback sent successfully'}), 200

@app.route('/received_feedbacks', methods=['GET'])
@login_required
def received_feedbacks():
    print('current_user', dir(current_user))
    if not current_user.is_authenticated:
        return redirect(url_for("register"))

    user = User.query.get(current_user.user_id)

    if not user:
        return redirect(url_for("register"))

    feedbacks = Feedback.query.filter_by(recipient_email=current_user.email).all()
    feedback_list = [
        {'id': fb.id, 'content': fb.content, 'status': fb.status, 'reply': fb.reply} for fb in feedbacks
    ]

    return jsonify({'feedbacks': feedback_list}), 200

@app.route('/update_feedback_status', methods=['POST'])
def update_feedback_status():
    auth_error = authenticate_request()
    if auth_error:
        return auth_error

    data = request.get_json()
    feedback_id = data.get('feedback_id')
    status = data.get('status')

    feedback = Feedback.query.get(feedback_id)

    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404

    feedback.status = status
    db.session.commit()
    return jsonify({'message': 'Feedback status updated successfully'}), 200

@app.route('/reply_feedback', methods=['POST'])
def reply_feedback():
    data = request.get_json()
    feedback_id = data.get('feedback_id')
    reply = data.get('reply')

    feedback = Feedback.query.get(feedback_id)

    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404

    feedback.reply = reply
    db.session.commit()
    return jsonify({'message': 'Feedback reply sent successfully'}), 200

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
