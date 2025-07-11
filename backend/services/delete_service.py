import os
from sqlalchemy.orm import Session
from models import User, Subscription, AnalysisLog
from stripe_app import cancel_subscription_by_customer_id
from db import get_db  # 必要に応じて修正

def delete_user_account(email: str, db: Session):
    # ユーザー取得
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"success": False, "message": "ユーザーが見つかりません"}

    user_id = user.id

    # Stripeのサブスクリプションをキャンセル
    if user.stripe_customer_id:
        cancel_subscription_by_customer_id(user.stripe_customer_id)

    # 保存済みJSONファイルを削除
    logs = db.query(AnalysisLog).filter(AnalysisLog.user_id == user_id).all()
    for log in logs:
        if log.result_path and os.path.exists(log.result_path):
            try:
                os.remove(log.result_path)
            except Exception as e:
                print(f"[WARN] JSON削除失敗: {log.result_path} -> {e}")

    # 関連テーブル削除（外部キー制約の順に注意）
    db.query(AnalysisLog).filter(AnalysisLog.user_id == user_id).delete()
    db.query(Subscription).filter(Subscription.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()

    db.commit()

    return {"success": True, "message": "ユーザーと関連データを削除しました"}
