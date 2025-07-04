# test_db.py
from db import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("✅ DB接続成功:", version)
    cur.close()
    conn.close()
except Exception as e:
    print("🟥 DB接続失敗:", e)
