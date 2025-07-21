from models.analysis_log_model import AnalysisLog
from sqlalchemy_db import SessionLocal
from datetime import datetime

def save_analysis_log(user_id, video_url, video_title, platform, duration_sec,
                      comment_count, result_path, thumbnail_url=None,
                      success=True, error_message=None):  # ← ここに追加
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
            thumbnail_url=thumbnail_url,  # ← ここにも追加
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
