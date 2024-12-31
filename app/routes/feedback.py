from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Feedback
from app.extensions import db
from app.utils.moderation import moderate_feedback

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@bp.route('/', methods=['POST'])
@jwt_required()
def send_feedback():
    data = request.json
    if "inappropriate" in moderate_feedback(data['feedback']).lower():
        return jsonify({'message': 'Feedback contains inappropriate content.'}), 400

    sentiment = 'Positive' if "good" in data['feedback'] else 'Negative'
    new_feedback = Feedback(recipient=data['recipient'], feedback=data['feedback'], sentiment=sentiment)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback sent successfully!', 'sentiment': sentiment}), 201
