from sqlalchemy_db import SessionLocal
from models.user_model import User

def get_user_id_by_email(email: str) -> int | None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user.id if user else None
    finally:
        db.close()
