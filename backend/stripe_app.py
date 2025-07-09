# stripe_app.py

from flask import Flask, jsonify
from flask_cors import CORS
from services.stripe_service import create_checkout_session
from flask import request
import stripe
import os
from dotenv import load_dotenv
from sqlalchemy_db import SessionLocal
from models.user_model import User
from models.subscription_model import Subscription
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

print("[DEBUG] stripe_app.py loaded")

# stripe_app.py の該当箇所
@app.route("/create-checkout-session", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"error": "メールアドレスが必要です"}), 400

        session = create_checkout_session(email)
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    



load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # 念のためセット
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")  # Webhook Secret

def stripe_timestamp_to_datetime(ts):
    return datetime.utcfromtimestamp(ts)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        print("❌ Webhook signature invalid")
        return jsonify({"error": "Invalid signature"}), 400

    print(f"📨 Received event: {event['type']}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("🔍 Session content:", session)

        email = session.get("customer_email")
        print("📧 Extracted email:", email)

        # このあとも try で囲って原因を isolation できるように
        try:
            db = SessionLocal()
            user = db.query(User).filter_by(email=email).first()
            if not user:
                print("❌ No user found")
                return jsonify({"error": "User not found"}), 404

            sub = db.query(Subscription).filter_by(user_id=user.id).first()
            if not sub:
                sub = Subscription(user_id=user.id)
                db.add(sub)

            sub.plan = "pro"
            sub.status = "trialing"
            sub.start_date = stripe_timestamp_to_datetime(session["created"])
            sub.updated_at = datetime.utcnow()

            db.commit()
            print(f"✅ Subscription updated for {email}")
        except Exception as e:
            print(f"🔥 Error updating subscription: {e}")
            return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"})


