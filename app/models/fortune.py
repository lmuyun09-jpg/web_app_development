from .db import get_db_connection
from datetime import datetime

class Fortune:
    """
    籤詩 Model，儲存籤詩的基本資料庫
    """
    @staticmethod
    def create(data):
        """
        新增一首籤詩記錄
        :param data: 字典形式的資料 (需包含 title, content, description)
        :return: 建立成功回傳 id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO fortunes (title, content, description, created_at) VALUES (?, ?, ?, ?)",
                (data.get('title'), data.get('content'), data.get('description'), created_at)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Fortune.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(id):
        """
        根據 ID 取得單首籤詩
        :param id: 籤詩 ID
        :return: 籤詩資料字典，或 None
        """
        try:
            conn = get_db_connection()
            fortune = conn.execute("SELECT * FROM fortunes WHERE id = ?", (id,)).fetchone()
            return dict(fortune) if fortune else None
        except Exception as e:
            print(f"Error in Fortune.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all():
        """
        取得所有的籤詩列表
        :return: 籤詩字典串列
        """
        try:
            conn = get_db_connection()
            fortunes = conn.execute("SELECT * FROM fortunes").fetchall()
            return [dict(f) for f in fortunes]
        except Exception as e:
            print(f"Error in Fortune.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_random():
        """
        隨機取得一首籤詩，用於抽籤核心功能
        :return: 單筆籤詩字典，或 None
        """
        try:
            conn = get_db_connection()
            fortune = conn.execute("SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1").fetchone()
            return dict(fortune) if fortune else None
        except Exception as e:
            print(f"Error in Fortune.get_random: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(id, data):
        """
        更新籤詩記錄
        :param id: 籤詩 ID
        :param data: 字典形式欲更新的內容
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            fields = []
            params = []
            for key in ['title', 'content', 'description']:
                if key in data:
                    fields.append(f"{key} = ?")
                    params.append(data[key])
            
            if not fields:
                return False

            params.append(id)
            query = f"UPDATE fortunes SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Fortune.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(id):
        """
        刪除籤詩記錄
        :param id: 籤詩 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM fortunes WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Fortune.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
