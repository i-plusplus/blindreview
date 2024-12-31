from flask import Blueprint, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from app.models import Feedback

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/<recipient>', methods=['GET'])
def get_analytics(recipient):
    feedbacks = Feedback.query.filter_by(recipient=recipient).all()
    sentiments = [fb.sentiment for fb in feedbacks]
    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}

    plt.figure(figsize=(6, 4))
    plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'red', 'gray'])
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return jsonify({'plot': plot_data})
