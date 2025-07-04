# test_insert_user.py
from db import get_connection

def upsert_user(google_id, name, email):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (google_id, name, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (google_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                updated_at = CURRENT_TIMESTAMP;
        """, (google_id, name, email))

        conn.commit()
        print("✅ ユーザー登録成功")
    except Exception as e:
        print("🟥 ユーザー登録失敗:", e)
    finally:
        cur.close()
        conn.close()

# テスト用ユーザー情報（適当でOK）
upsert_user("test-google-id-123", "テスト太郎", "test@example.com")
