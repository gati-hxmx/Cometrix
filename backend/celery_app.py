# backend/celery_app.py
#
# Celeryアプリの唯一の定義箇所。タスク自体は tasks/chat_tasks.py 側で
# @celery_app.task を使って登録する(このモジュールをimportして使う)。
# ワーカー起動: celery -A celery_app worker --loglevel=info

from celery import Celery

celery_app = Celery(
    "cometrix",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks.chat_tasks"],
)
