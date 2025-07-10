# tests/test_log_service.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from sqlalchemy_db import Base, engine, SessionLocal
from models.analysis_log_model import AnalysisLog
from models.user_model import User  # 👈 これを忘れずに import！

from services.log_service import save_analysis_log

from sqlalchemy_db import engine

print("✅ Using DB URL:", engine.url)


# 1. テーブル作成
Base.metadata.create_all(bind=engine)

# 2. ダミーユーザー追加（外部キー用）
db = SessionLocal()
# 既に同じ google_id を持つユーザーがいれば削除
existing = db.query(User).filter_by(google_id="test_google_id").first()
if existing:
    db.delete(existing)
    db.commit()

# ユーザーを作成
test_user = User(
    id=9999,
    google_id="test_google_id",
    email="test1@example.com",
    name="テストユーザー"
)
db.add(test_user)
db.commit()

# 3. ログ保存テスト
save_analysis_log(
    user_id=999,
    video_url="https://www.youtube.com/watch?v=test123",
    video_title="テスト動画",
    platform="youtube",
    duration_sec=360,
    comment_count=42,
    result_path="backend/chat_data/youtube_test123.json"
)
