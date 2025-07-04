from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_dance.contrib.google import google
from config import Config
from auth.oauth import create_google_blueprint
from models.user import User
from db import upsert_user 

app = Flask(__name__)
app.config.from_object(Config)

# 🔑 セッションが効くように
app.secret_key = app.config.get("SECRET_KEY", "dev")

# ユーザー保存用
user_store = {}

# 認証ルート登録
google_bp = create_google_blueprint()
app.register_blueprint(google_bp, url_prefix="/login")

# Flask-Login 初期化
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
    upsert_user(user.id, user.name, user.email) 
    user_store[user.id] = user
    login_user(user)
    upsert_user(user.id, user.name, user.email)
    return redirect("http://localhost:5173/")

# 認証成功後の処理
@app.route("/login/google/authorized")
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return redirect("http://localhost:5173/login?error=auth_failed")
    info = resp.json()
    user = User(id=info["id"], name=info["name"], email=info["email"])
    upsert_user(user.id, user.name, user.email)
    user_store[user.id] = user
    login_user(user)
    upsert_user(user.id, user.name, user.email)
    return redirect("http://localhost:5173/")

# 認証状態確認用API
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



# Flaskの最後に追加
from flask_cors import CORS
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


# backend/app.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data

app = FastAPI()

# 開発時CORS（必要に応じて絞る）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/chat-data")
def get_chat_data(videoId: str = Query(..., min_length=11, max_length=15)):
    try:
        return fetch_chat_data(videoId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"チャットデータの取得に失敗しました: {e}")
