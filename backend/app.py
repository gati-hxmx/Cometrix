from flask import Flask, redirect, url_for
from config import Config
from auth.oauth import create_google_blueprint
from flask_dance.contrib.google import google

app = Flask(__name__)
app.config.from_object(Config)

# 認証ルーター
google_bp = create_google_blueprint()
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        return f"こんにちは {resp.json()['email']} さん！"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))

#     try:
#         resp = google.get("/oauth2/v2/userinfo")
#         if not resp.ok:
#             return f"Google API error: {resp.text}", 500

#         email = resp.json().get("email", "不明")
#         return f"こんにちは {email} さん！"
#     except Exception as e:
#         return f"サーバーエラーが発生しました: {str(e)}", 500



@app.route("/authorize")  # このルート名は redirect_to="google_authorized" に対応
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]
    return f"こんにちは {email} さん！"

@app.route("/test")
def test():
    return "TEST OK"

