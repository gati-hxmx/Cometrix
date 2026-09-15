# backend/session_auth.py
#
# Flask(stripe_app.py)とFastAPI(api_app.py / routes/*)の両方から使う、
# 共通のセッション検証ロジック。
# ログインセッションはauth_app.py(Flask-Login)が管理しているため、
# リクエストのCookieをそのままauth_app.pyの /api/user に転送して検証し、
# 本人のメールアドレスを取得する。クライアントが送ってきたemailは信用しない。

import os
import requests

AUTH_APP_BASE = os.getenv("AUTH_APP_INTERNAL_URL", "http://localhost:5000")


class SessionAuthError(Exception):
    pass


def verify_session(cookie_header: str | None) -> str:
    if not cookie_header:
        raise SessionAuthError("ログインが必要です")

    try:
        resp = requests.get(
            f"{AUTH_APP_BASE}/api/user",
            headers={"Cookie": cookie_header},
            timeout=5,
        )
    except requests.RequestException:
        raise SessionAuthError("認証サーバーに接続できません")

    if resp.status_code != 200:
        raise SessionAuthError("ログインが必要です")

    email = resp.json().get("email")
    if not email:
        raise SessionAuthError("ログインが必要です")
    return email
