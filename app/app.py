import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from googletrans import Translator
from textblob import TextBlob
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/feedback/<recipient>', methods=['GET'])
def get_feedback(recipient):
    feedbacks = Feedback.query.filter_by(recipient=recipient).all()
    feedback_list = [
        {
            'id': fb.id,
            'feedback': fb.feedback,
            'reply': fb.reply,
            'status': fb.status
        }
        for fb in feedbacks
    ]
    return jsonify(feedback_list)

@app.route('/feedback/reply/<int:id>', methods=['POST'])
def reply_feedback(id):
    data = request.json
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({'message': 'Feedback not found'}), 404
    feedback.reply = data['reply']
    feedback.status = data['status']  # Accepted or Rejected
    db.session.commit()
    return jsonify({'message': 'Reply updated successfully!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



# Add JWT configuration
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Use a strong secret key
jwt = JWTManager(app)


# Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(username=data['username'], password=data['password'])  # Hash in production
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    token = create_access_token(identity=user.username)
    return jsonify({'token': token}), 200





# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
mail = Mail(app)

# Send Email Function
def send_email(recipient_email, subject, body):
    msg = Message(subject, recipients=[recipient_email], body=body, sender='your_email@gmail.com')
    mail.send(msg)


import openai

# Configure OpenAI API key
openai.api_key = "your_openai_api_key"

def moderate_feedback(feedback_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Moderate the following feedback for inappropriate content: {feedback_text}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

@app.route('/feedback', methods=['POST'])
@jwt_required()
def send_feedback():
    data = request.json
    moderation_result = moderate_feedback(data['feedback'])
    if "inappropriate" in moderation_result.lower():
        return jsonify({'message': 'Feedback contains inappropriate content and was rejected.'}), 400

    sentiment_score = TextBlob(data['feedback']).sentiment.polarity
    sentiment = 'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'

    new_feedback = Feedback(
        recipient=data['recipient'],
        feedback=data['feedback'],
        sentiment=sentiment
    )
    db.session.add(new_feedback)
    db.session.commit()
    # Send email notification to recipient
    recipient_email = f"{data['recipient']}@example.com"  # Replace with a real lookup
    send_email(
        recipient_email,
        "New Feedback Received",
        f"You've received new feedback: {data['feedback']}\nSentiment: {sentiment}"
    )

    return jsonify({'message': 'Feedback sent successfully!', 'sentiment': sentiment}), 201




# translator = Translator()
#
# @app.route('/translate', methods=['POST'])
# @jwt_required()
# def translate_feedback():
#     data = request.json
#     translated_text = translator.translate(data['text'], dest=data['language']).text
#     return jsonify({'translated_text': translated_text}), 200
#
# @app.route('/analytics/<recipient>', methods=['GET'])
# @jwt_required()
# def feedback_analytics(recipient):
#     feedbacks = Feedback.query.filter_by(recipient=recipient).all()
#     sentiments = [fb.sentiment for fb in feedbacks]
#
#     # Generate sentiment distribution plot
#     sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
#     plt.figure(figsize=(6, 4))
#     plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'red', 'gray'])
#     plt.title('Feedback Sentiment Distribution')
#     plt.xlabel('Sentiments')
#     plt.ylabel('Count')
#
#     # Save plot to buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
#     buffer.close()
#
#     return jsonify({'plot': plot_data})
