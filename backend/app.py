from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_dance.contrib.google import google
from flask_cors import CORS
from config import Config
from auth.oauth import create_google_blueprint
from models.user import User
from db_logic import upsert_user
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get("SECRET_KEY", "dev")  # 🔑 セッション用

# Blueprint登録（Google認証）
google_bp = create_google_blueprint()
app.register_blueprint(google_bp, url_prefix="/login")

# Flask-Loginの設定
login_manager = LoginManager()
login_manager.login_view = "google.login"
login_manager.init_app(app)

# ローカルユーザー保存用（セッション管理）
user_store = {}

@login_manager.user_loader
def load_user(user_id):
    return user_store.get(user_id)

# ------------------------
# 認証エントリポイント
# ------------------------
@app.route("/")
def index():
    print("🚪 / にアクセスされました")
    if not google.authorized:
        print("🟥 未認証 → ログイン画面へ")
        return redirect(url_for("google.login"))

    try:
        resp = google.get("/oauth2/v2/userinfo")
        if not resp.ok:
            print("🟥 ユーザー情報取得失敗:", resp.text)
            return "ユーザー情報の取得に失敗しました", 500

        info = resp.json()
        print("🖼️ Googleユーザー情報:", info)

        user = User(id=info["id"], name=info["name"], email=info["email"])
        upsert_user(user.id, user.name, user.email)
        user_store[user.id] = user
        login_user(user)

        return redirect("http://localhost:5173/")
    except Exception as e:
        print("🟥 例外:", e)
        return "内部エラー", 500

# ------------------------
# Google 認証成功後の処理
# ------------------------
@app.route("/login/google/authorized")
def google_authorized():
    print("📥 /login/google/authorized に到達✅")

    if not google.authorized:
        print("🟥 google.authorized = False")
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        print("🟥 ユーザー情報取得失敗:", resp.text)
        return redirect("http://localhost:5173/login?error=auth_failed")

    info = resp.json()
    print("🖼️ Googleユーザー情報:", info)

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

# ------------------------
# 認証関連 API
# ------------------------

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

# ------------------------
# CORS設定（開発用）
# ------------------------
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
