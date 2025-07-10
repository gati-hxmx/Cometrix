# log_service.py

from models.analysis_log_model import AnalysisLog
from sqlalchemy_db import SessionLocal
from datetime import datetime

def save_analysis_log(user_id, video_url, video_title, platform, duration_sec,
                      comment_count, result_path, success=True, error_message=None):
    db = SessionLocal()
    try:
        log = AnalysisLog(
            user_id=user_id,
            video_url=video_url,
            video_title=video_title,
            platform=platform,
            duration_sec=duration_sec,
            comment_count=comment_count,
            result_path=result_path,
            analyzed_at=datetime.utcnow(),
        )
        db.add(log)
        db.commit()
        print("✅ 分析ログ保存成功")
    except Exception as e:
        import traceback; traceback.print_exc()
        print("🟥 分析ログ保存失敗:", e)
    finally:
        db.close()
