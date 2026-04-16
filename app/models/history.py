from .db import get_db_connection
from datetime import datetime

class History:
    @staticmethod
    def create(user_id, fortune_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO history (user_id, fortune_id, created_at) VALUES (?, ?, ?)",
            (user_id, fortune_id, created_at)
        )
        conn.commit()
        history_id = cursor.lastrowid
        conn.close()
        return history_id

    @staticmethod
    def get_by_id(history_id):
        conn = get_db_connection()
        history = conn.execute("SELECT * FROM history WHERE id = ?", (history_id,)).fetchone()
        conn.close()
        return dict(history) if history else None

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        # 可以用 JOIN 來獲取對應的籤詩資料
        query = '''
            SELECT h.id as history_id, h.created_at, f.*
            FROM history h
            JOIN fortunes f ON h.fortune_id = f.id
            WHERE h.user_id = ?
            ORDER BY h.created_at DESC
        '''
        records = conn.execute(query, (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def get_all():
        conn = get_db_connection()
        records = conn.execute("SELECT * FROM history").fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def delete(history_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM history WHERE id = ?", (history_id,))
        conn.commit()
        conn.close()
        return True
