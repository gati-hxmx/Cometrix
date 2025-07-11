from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_dance.contrib.google import google
from config import Config
from auth.oauth import create_google_blueprint
from models.user import User
from db_logic import upsert_user 
from datetime import datetime

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
    print("🚪 / にアクセスされました")

    if not google.authorized:
        print("🟥 google.authorized = False → ログイン画面へリダイレクト")
        return redirect(url_for("google.login"))

    print("🔐 google.authorized = True")

    try:
        resp = google.get("/oauth2/v2/userinfo")
        if not resp.ok:
            print("🟥 ユーザー情報の取得に失敗:", resp.text)
            return "ユーザー情報の取得に失敗しました", 500

        info = resp.json()
        print("🖼️ Googleユーザー情報:", info)

        user = User(id=info["id"], name=info["name"], email=info["email"])
        print("👤 User オブジェクト作成:", user)

        upsert_user(user.id, user.name, user.email)
        print("✅ ユーザー情報をDBに upsert 完了")

        user_store[user.id] = user
        print("💾 ユーザー情報を user_store に保存")

        login_user(user)
        print("🔓 login_user 実行完了")

        return redirect("http://localhost:5173/")
    except Exception as e:
        print("🟥 例外発生:", e)
        return "内部エラー", 500


# 認証成功後の処理
from datetime import datetime

@app.route("/login/google/authorized")
def google_authorized():
    print("📥 /login/google/authorized に到達✅")

    if not google.authorized:
        print("🟥 google.authorized = False")
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        print("🟥 ユーザー情報取得に失敗:", resp.text)
        return redirect("http://localhost:5173/login?error=auth_failed")

    info = resp.json()
    print("🖼️ Googleユーザー情報:", info)  # ← これが出るか確認

    user = User(
        id=info["id"],
        name=info["name"],
        email=info["email"]
    )

    user_store[user.id] = user
    login_user(user)

    upsert_user(
        user_id=user.id,
        name=user.name,
        email=user.email,
        profile_image_url=info.get("picture"),
        last_login_at=datetime.utcnow()
    )

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


