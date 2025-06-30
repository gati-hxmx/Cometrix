# auth_app.py
from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_dance.contrib.google import google
from config import Config
from auth.oauth import create_google_blueprint
from models.user import User
from flask_cors import CORS

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
    user_store[user.id] = user
    login_user(user)
    return redirect("http://localhost:5173/")

@app.route("/login/google/authorized")
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return redirect("http://localhost:5173/login?error=auth_failed")
    info = resp.json()
    user = User(id=info["id"], name=info["name"], email=info["email"])
    user_store[user.id] = user
    login_user(user)
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
    return jsonify({"message": "Logged out"}), 200

# CORS
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
