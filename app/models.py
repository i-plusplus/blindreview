from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)
    reply = db.Column(db.String(500), nullable=True)
    sentiment = db.Column(db.String(50), nullable=False)  # Sentiment analysis result
    status = db.Column(db.String(50), default='Pending')  # Pending, Accepted, Rejected

