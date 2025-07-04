# db_logic.py
from db import get_connection

# db_logic.py の中を db.py のバージョンに揃える


def upsert_user(user_id, name, email):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (google_id, name, email)
            VALUES (%s, %s, %s)
            ON CONFLICT (google_id)
            DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email, updated_at = CURRENT_TIMESTAMP;
        """, (user_id, name, email))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ ユーザー登録/更新 完了")
    except Exception as e:
        print("🟥 ユーザー登録失敗:", e)


def upsert_subscription(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 既に存在するか確認
        cur.execute("SELECT id FROM subscriptions WHERE user_id = %s", (user_id,))
        result = cur.fetchone()

        if result:
            # すでに存在 → statusを更新（必要に応じて）
            cur.execute("""
                UPDATE subscriptions
                SET updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """, (user_id,))
            print(f"✅ サブスクリプション（更新）: user_id={user_id}")
        else:
            # 存在しない → 新規登録
            cur.execute("""
                INSERT INTO subscriptions (user_id, plan, status)
                VALUES (%s, 'free', 'active')
            """, (user_id,))
            print(f"✅ サブスクリプション（新規登録）: user_id={user_id}")

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("🟥 サブスクリプション登録失敗:", e)


def get_active_subscription(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT plan, status, start_date, end_date
            FROM subscriptions
            WHERE user_id = %s AND status = 'active'
            ORDER BY start_date DESC
            LIMIT 1;
        """, (user_id,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return {
                "plan": row[0],
                "status": row[1],
                "start_date": row[2],
                "end_date": row[3]
            }
        else:
            return None
    except Exception as e:
        print("🟥 サブスクリプション取得失敗:", e)
        return None


def get_user_db_id(google_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM users WHERE google_id = %s", (google_id,))
        result = cur.fetchone()
        return result[0] if result else None
    finally:
        cur.close()
        conn.close()

