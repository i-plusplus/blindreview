from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy database for users (in real applications, use a real database)
users_db = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Load user function
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users_db.values() if user.username == username), None)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('verify_otp.html')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Profile route (protected)
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        user_id = str(len(users_db) + 1)  # Simple ID assignment, use UUID or DB ID in real applications
        new_user = User(user_id, username, password_hash)
        users_db[user_id] = new_user
        login_user(new_user)
        return redirect(url_for('profile'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
