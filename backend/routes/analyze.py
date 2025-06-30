# routes/analyze.py

from flask import Blueprint, request, jsonify
from services.yt_comment import extract_comments

bp = Blueprint('analyze', __name__)

@bp.route('/api/comments', methods=['POST'])
def get_comments():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        comments = extract_comments(url)
        return jsonify({'comments': comments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
