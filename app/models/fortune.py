from .db import get_db_connection
from datetime import datetime

class Fortune:
    @staticmethod
    def create(title, content, description):
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO fortunes (title, content, description, created_at) VALUES (?, ?, ?, ?)",
            (title, content, description, created_at)
        )
        conn.commit()
        fortune_id = cursor.lastrowid
        conn.close()
        return fortune_id

    @staticmethod
    def get_by_id(fortune_id):
        conn = get_db_connection()
        fortune = conn.execute("SELECT * FROM fortunes WHERE id = ?", (fortune_id,)).fetchone()
        conn.close()
        return dict(fortune) if fortune else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        fortunes = conn.execute("SELECT * FROM fortunes").fetchall()
        conn.close()
        return [dict(f) for f in fortunes]

    @staticmethod
    def get_random():
        conn = get_db_connection()
        # 利用 SQLite 內建的 RANDOM() 隨機取得一筆
        fortune = conn.execute("SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1").fetchone()
        conn.close()
        return dict(fortune) if fortune else None

    @staticmethod
    def update(fortune_id, title=None, content=None, description=None):
        conn = get_db_connection()
        fields = []
        params = []
        if title:
            fields.append("title = ?")
            params.append(title)
        if content:
            fields.append("content = ?")
            params.append(content)
        if description:
            fields.append("description = ?")
            params.append(description)

        if not fields:
            return False

        params.append(fortune_id)
        query = f"UPDATE fortunes SET {', '.join(fields)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(fortune_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM fortunes WHERE id = ?", (fortune_id,))
        conn.commit()
        conn.close()
        return True
