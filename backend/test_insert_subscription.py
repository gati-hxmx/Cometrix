# test_insert_subscription.py

from db_logic import upsert_subscription
from dotenv import load_dotenv

load_dotenv()

# 例: 実際に存在する user_id を使う（users テーブルに入っているID）
test_user_id = 2  # ← あなたのDBに存在するIDに置き換えてください

upsert_subscription(test_user_id)
