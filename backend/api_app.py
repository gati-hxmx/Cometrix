# api_app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from services.yt_chat import fetch_chat_data

app = FastAPI()

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
