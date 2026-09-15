# backend/auth_dependency.py
#
# FastAPI(api_app.py / routes/*)用の認証依存関数。
# 実体は session_auth.py の共通ロジック(Flask側stripe_app.pyとも共有)。

from fastapi import Request, HTTPException
from session_auth import verify_session, SessionAuthError


def get_current_email(request: Request) -> str:
    try:
        return verify_session(request.headers.get("cookie"))
    except SessionAuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
