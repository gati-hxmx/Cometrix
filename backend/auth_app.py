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
    upsert_user(user.id, user.name, user.email)
    upsert_subscription(user.id)
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
    user.db_id = get_user_db_id(user.id)
    user_store[user.id] = user
    login_user(user)
    upsert_user(user.id, user.name, user.email)
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
    return jsonify({"message": "Logged out"}), 200

# CORS
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

@app.route("/api/subscription")
def get_subscription():
    if not current_user.is_authenticated:
        print("🟥 current_user is not authenticated")
        return jsonify({'error': 'unauthorized'}), 401

    try:
        print("🔍 current_user:", current_user)
        print("🔍 current_user.id:", current_user.id)
        print("🔍 current_user.name:", current_user.name)
        print("🔍 current_user.email:", current_user.email)

        # db_id があるかを確認（Flask-Login によって User クラスの属性が維持されてるか）
        if not hasattr(current_user, 'db_id'):
            print("🟥 current_user.db_id が存在しません")
            return jsonify({'error': 'db_id_missing'}), 500

        print("✅ current_user.db_id:", current_user.db_id)

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
        print('🟥 サブスクリプション取得失敗:', repr(e))
        return jsonify({'error': 'internal_error'}), 500
    
@login_manager.user_loader
def load_user(user_id):
    print(f"🔍 user_loader 呼び出し: user_id={user_id}")
    user = user_store.get(user_id)
    print(f"🔍 user_store から復元されたユーザー: {user}")
    return user




