from fastapi import APIRouter, HTTPException
from services.user_service import get_user_id_by_email
from services.billing_service import get_billing_history_by_user_id

router = APIRouter(prefix="/api/billing", tags=["Billing"])


@router.get("/history")
def get_billing_history(email: str):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    history = get_billing_history_by_user_id(user_id)
    return history
