# api_app.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import subprocess
import json

# --- Services ---
from services.yt_chat import fetch_chat_data as fetch_youtube_chat_data
from services.twitch_chat import fetch_chat_data as fetch_twitch_chat_data
from services.user_service import get_user_id_by_email
from services.delete_service import delete_user_account
from auth_dependency import get_current_email

# --- DB ---
from sqlalchemy_db import get_db

# --- App Setup ---
app = FastAPI()
CHAT_DATA_DIR = "chat_data"  # 保存先パス

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Schemas ---
class ChatDataRequest(BaseModel):
    videoId: str


# --- YouTube チャット取得 ---
@app.post("/api/chat-data")
def get_chat_data_post(data: ChatDataRequest, email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    try:
        # ✅ 毎回 fetch_youtube_chat_data を通すことでログも必ず保存される
        return fetch_youtube_chat_data(video_id=data.videoId, user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"チャットデータの取得に失敗しました: {e}"
        )


# --- Twitch チャット取得 ---
@app.post("/api/chat-data/twitch")
def get_twitch_chat_data_post(data: ChatDataRequest, email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    os.makedirs(CHAT_DATA_DIR, exist_ok=True)
    raw_path = os.path.join(CHAT_DATA_DIR, f"{data.videoId}.json")

    # ✅ ファイルがあれば読み込み（エラー時は再取得）
    if os.path.exists(raw_path):
        try:
            print("[INFO] Twitch 整形済みファイルを返却✅")
            return fetch_twitch_chat_data(raw_path, data.videoId, user_id)
        except Exception as e:
            print(f"[WARN] 整形済みファイルの読み込み失敗: {e}")
            # → 続行して再取得

    # ✅ なければダウンロードして整形
    try:
        subprocess.run(
            [
                "./TwitchDownloaderCLI/TwitchDownloaderCLI",
                "chatdownload",
                "--id",
                data.videoId,
                "--output",
                raw_path,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500, detail=f"Twitchチャットのダウンロードに失敗しました: {e}"
        )

    try:
        return fetch_twitch_chat_data(raw_path, data.videoId, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Twitchチャットの整形に失敗しました: {e}"
        )


# --- 退会処理 ---
@app.post("/api/delete-account")
def delete_account(db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    try:
        delete_user_account(db=db, user_id=user_id)
        return {"message": "アカウントを削除しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"退会処理に失敗しました: {str(e)}")


from routes.analyze import router as analyze_router

app.include_router(analyze_router, prefix="/api/analyze")


from models.analysis_log_model import AnalysisLog  # ✅ OK


@app.get("/api/analysis/history")
def get_analysis_history(db: Session = Depends(get_db), email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    logs = (
        db.query(AnalysisLog)
        .filter_by(user_id=user_id)
        .order_by(AnalysisLog.analyzed_at.desc())
        .all()
    )
    return [log.to_dict() for log in logs]


from routes import billing

app.include_router(billing.router)
