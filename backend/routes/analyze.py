# backend/routes/analyze.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tasks.chat_tasks import analyze_youtube_chat_task
from celery.result import AsyncResult
from celery_app import celery_app
from services.user_service import get_user_id_by_email

router = APIRouter()

class AnalyzeRequest(BaseModel):
    videoId: str
    email: str

# backend/routes/analyze.py

@router.post("/youtube/async")
def analyze_youtube_async(request: AnalyzeRequest):
    user_id = get_user_id_by_email(request.email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    full_url = f"https://www.youtube.com/watch?v={request.videoId}"  # ←ここで組み立てる
    task = analyze_youtube_chat_task.delay(full_url, user_id)
    return {"task_id": task.id}



@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
