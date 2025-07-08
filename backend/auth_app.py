# auth_app.py
from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_dance.contrib.google import google
from config import Config
from auth.oauth import create_google_blueprint
from models.user import User
from flask_cors import CORS
from db_logic import upsert_user
from db_logic import upsert_user, upsert_subscription
from db_logic import get_active_subscription
from flask import jsonify
from flask_login import current_user
from db_logic import get_user_db_id
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get("SECRET_KEY", "dev")

user_store = {}

google_bp = create_google_blueprint()
app.register_blueprint(google_bp, url_prefix="/login")

login_manager = LoginManager()
login_manager.login_view = "google.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user_store.get(user_id)

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "ユーザー情報の取得に失敗しました", 500

    info = resp.json()
    user = User(id=info["id"], name=info["name"], email=info["email"])
    user.db_id = get_user_db_id(user.id)
    user_store[user.id] = user
    login_user(user)
    upsert_user(user.id, user.name, user.email, user.profile_image_url, user.last_login_at)
    upsert_subscription(user.id)
    return redirect("http://localhost:5173/")

@app.route("/login/google/authorized")
def google_authorized():
    print("📥 /login/google/authorized に到達")
    if not google.authorized:
        print("🟥 google.authorized = False")
        return redirect("http://localhost:5173/")

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        print("🟥 ユーザー情報取得に失敗:", resp.text)
        return redirect("http://localhost:5173/login?error=auth_failed")

    info = resp.json()
    print("✅ ユーザー情報取得:", info)
    user = User(id=info["id"], name=info["name"], email=info["email"])
    user.db_id = get_user_db_id(user.id)
    user_store[user.id] = user
    login_user(user)
    upsert_user(user.id, user.name, user.email, user.profile_image_url, user.last_login_at)
    upsert_subscription(user.id)
    return redirect("http://localhost:5173/")

@app.route("/api/userinfo")
def userinfo():
    if not google.authorized:
        return jsonify({"error": "Unauthorized"}), 401
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info"}), 500
    return jsonify(resp.json())

@app.route("/api/user")
def get_user():
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({
        'name': current_user.name,
        'email': current_user.email
    })

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return '', 204  # ←空を返すことでフロントの fetch が .json() を要求しない


# CORS
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

@app.route("/api/subscription")
def get_subscription():
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT plan, status FROM subscriptions WHERE user_id = %s ORDER BY id DESC LIMIT 1", (current_user.db_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify({
                'plan': result[0],
                'status': result[1]
            })
        else:
            return jsonify({'plan': 'free', 'status': 'inactive'})  # ← デフォルト
    except Exception as e:
        print('🟥 サブスクリプション取得失敗:', e)
        return jsonify({'error': 'internal_error'}), 500



