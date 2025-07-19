# backend/celery_app.py

from celery import Celery

celery_app = Celery(
    "cometrix_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.chat_tasks.analyze_youtube_chat": {"queue": "youtube"},
    "tasks.chat_tasks.analyze_twitch_chat": {"queue": "twitch"},
}





