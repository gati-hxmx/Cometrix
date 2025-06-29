from flask_dance.contrib.google import make_google_blueprint
import os

# oauth.py

# def create_google_blueprint():
#     return make_google_blueprint(
#         client_id=None,
#         client_secret=None,
#         scope=["profile", "email"],
#         redirect_url="http://localhost:5000/login/google/authorized"  # デフォルトのパス
#     )

def create_google_blueprint():
    return make_google_blueprint(
        client_id=None,
        client_secret=None,
        scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
    )
