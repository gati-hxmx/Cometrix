from fastapi import APIRouter, HTTPException, Depends
from services.user_service import get_user_id_by_email
from services.billing_service import get_billing_history_by_user_id
from auth_dependency import get_current_email

router = APIRouter(prefix="/api/billing", tags=["Billing"])


@router.get("/history")
def get_billing_history(email: str = Depends(get_current_email)):
    user_id = get_user_id_by_email(email)
    if user_id is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    history = get_billing_history_by_user_id(user_id)
    return history
