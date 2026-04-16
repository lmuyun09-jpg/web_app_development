from .db import get_db_connection
from datetime import datetime

class History:
    """
    抽籤歷史紀錄 Model，存放使用者過去的算命結果
    """
    @staticmethod
    def create(data):
        """
        新增一筆抽籤歷史紀錄
        :param data: 包含 'user_id' 與 'fortune_id' 的字典
        :return: 建立成功回傳 id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO history (user_id, fortune_id, created_at) VALUES (?, ?, ?)",
                (data.get('user_id'), data.get('fortune_id'), created_at)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in History.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(id):
        """
        根據 ID 取得單筆抽籤歷史紀錄
        :param id: 歷史紀錄 ID
        :return: 字典資料，含 user_id, fortune_id, created_at 等
        """
        try:
            conn = get_db_connection()
            record = conn.execute("SELECT * FROM history WHERE id = ?", (id,)).fetchone()
            return dict(record) if record else None
        except Exception as e:
            print(f"Error in History.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得某位特定用戶所有的抽籤歷史紀錄，並加入關聯的籤詩標題與內容
        :param user_id: 用戶 ID
        :return: 歷史紀錄的串列
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT h.id as history_id, h.created_at, f.*
                FROM history h
                JOIN fortunes f ON h.fortune_id = f.id
                WHERE h.user_id = ?
                ORDER BY h.created_at DESC
            '''
            records = conn.execute(query, (user_id,)).fetchall()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error in History.get_by_user_id: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all():
        """
        取得所有的抽籤歷史紀錄
        :return: 紀錄串列
        """
        try:
            conn = get_db_connection()
            records = conn.execute("SELECT * FROM history").fetchall()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error in History.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(id, data):
        """
        更新這筆歷史紀錄 (實際上歷史紀錄為唯讀，此函式供符合規格之實作預留)
        :param id: 歷史紀錄 ID
        :param data: 欲更新的資料
        :return: 無法更新時固定回傳 False 或照邏輯更新
        """
        try:
            conn = get_db_connection()
            fields = []
            params = []
            
            if 'fortune_id' in data:
                fields.append("fortune_id = ?")
                params.append(data['fortune_id'])

            if not fields:
                return False

            params.append(id)
            query = f"UPDATE history SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in History.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(id):
        """
        刪除特定抽籤歷史紀錄
        :param id: 紀錄 ID
        :return: 布林值代表成功與否
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM history WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in History.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
