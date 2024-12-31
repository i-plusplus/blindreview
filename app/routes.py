from flask import request, jsonify, render_template
from app import app, db
from app.models import Feedback
from app.utils import analyze_sentiment, moderate_content

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def send_feedback():
    data = request.json
    feedback = Feedback(content=data['content'], recipient=data['recipient'])
    sentiment = analyze_sentiment(data['content'])

    if moderate_content(data['content']):
        return jsonify({'message': 'Inappropriate content detected'}), 400

    feedback.sentiment = sentiment
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback sent successfully'})

@app.route('/analytics/<recipient>', methods=['GET'])
def get_analytics(recipient):
    feedbacks = Feedback.query.filter_by(recipient=recipient).all()
    sentiments = [f.sentiment for f in feedbacks]
    return jsonify({'feedback_count': len(feedbacks), 'sentiments': sentiments})