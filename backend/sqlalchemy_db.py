# # backend/sqlalchemy_db.py

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from dotenv import load_dotenv

# import os

# CELERY_MODE = os.getenv("CELERY_MODE") == "1"

# if CELERY_MODE:
#     print("🔃 CELERY_MODE=1 → DB無効化中")
#     engine = None
#     SessionLocal = None

#     # ダミーのBase定義（モデル宣言時にエラーを出さないため）
#     class DummyBase:
#         metadata = None

#     Base = DummyBase
# else:
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import sessionmaker, declarative_base

#     DATABASE_URL = os.environ.get("DATABASE_URL")
#     if not DATABASE_URL:
#         raise ValueError("❌ DATABASE_URL が未設定です。")

#     engine = create_engine(DATABASE_URL)
#     SessionLocal = sessionmaker(bind=engine)
#     Base = declarative_base()



# load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()


# from contextlib import contextmanager
# from typing import Generator

# # FastAPIのDepends用
# def get_db() -> Generator:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# backend/sqlalchemy_db.py
import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
load_dotenv()

CELERY_MODE = os.getenv("CELERY_MODE") == "1"

if CELERY_MODE:
    print("🔃 CELERY_MODE=1 → DB無効化中")
    engine = None
    SessionLocal = None

    class DummyBase:
        metadata = None
    Base = DummyBase

else:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if not DB_HOST or not DB_PORT or not DB_USER:
        raise ValueError("❌ .envのDB接続情報が不足しています")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base = declarative_base()

# 共通で使える get_db
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
