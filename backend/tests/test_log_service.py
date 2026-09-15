# tests/test_log_service.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest

from sqlalchemy_db import Base, engine, SessionLocal
from models.analysis_log_model import AnalysisLog
from models.user_model import User
from services.log_service import save_analysis_log


@pytest.fixture
def test_user():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    db.query(User).filter_by(google_id="test_google_id").delete()
    db.commit()

    user = User(google_id="test_google_id", email="test-log-service@example.com", name="テストユーザー")
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()

    yield user_id

    db = SessionLocal()
    db.query(AnalysisLog).filter_by(user_id=user_id).delete()
    db.query(User).filter_by(id=user_id).delete()
    db.commit()
    db.close()


def test_save_analysis_log_persists_row(test_user):
    user_id = test_user

    save_analysis_log(
        user_id=user_id,
        video_url="https://www.youtube.com/watch?v=test123",
        video_title="テスト動画",
        platform="youtube",
        duration_sec=360,
        comment_count=42,
        result_path="backend/chat_data/youtube_test123.json",
    )

    db = SessionLocal()
    logs = db.query(AnalysisLog).filter_by(user_id=user_id).all()
    db.close()

    assert len(logs) == 1
    assert logs[0].video_title == "テスト動画"
    assert logs[0].platform == "youtube"
    assert logs[0].comment_count == 42
