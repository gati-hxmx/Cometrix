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
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return f"こんにちは {resp.json()['email']} さん！"
