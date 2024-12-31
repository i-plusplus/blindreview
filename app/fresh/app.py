from flask import Flask
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, render_template
from email_sender import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# In-memory store for simplicity
users = {}
otp_store = {}

# Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users.get(data['email'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/')
def home():
    return render_template('register.html')


# Route to send OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email is required!'}), 400

    otp = '123456'  # Replace with a generated OTP logic
    otp_store[email] = otp
    # Simulate sending OTP (e.g., via email service)
    send_email(otp)

    print(f"Sending OTP {otp} to {email}")
    return jsonify({'message': 'OTP sent successfully!'}), 200

# Route to verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    if otp_store.get(email) == otp:
        users[email] = {'email': email}
        del otp_store[email]
        return jsonify({'message': 'OTP verified successfully!'}), 200
    return jsonify({'message': 'Invalid OTP!'}), 400

# Route to login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Simplified password check for demonstration
    if email in users and password == 'password':
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

# Protected route example
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Welcome {current_user["email"]}!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
