# stripe_app.py

from flask import Flask, jsonify
from flask_cors import CORS
from services.stripe_service import create_checkout_session

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

print("[DEBUG] stripe_app.py loaded")

@app.route("/create-checkout-session", methods=["POST"])
def checkout():
    try:
        session = create_checkout_session()
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
