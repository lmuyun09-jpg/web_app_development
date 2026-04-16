from .db import get_db_connection
from datetime import datetime

class Donation:
    """
    香油錢捐款 Model，紀錄與處理使用者的捐款資訊與狀態
    """
    @staticmethod
    def create(data):
        """
        新增一筆捐款紀錄
        :param data: 包含 'user_id', 'amount' (與選用的 'status') 的資料字典
        :return: 建立成功回傳 id，失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            
            # 使用者可以為非會員(NULL)，但目前架構設計為外鍵，如果無 user_id 端看設計而定。
            user_id = data.get('user_id')
            amount = data.get('amount')
            status = data.get('status', 'PENDING')
            
            cursor.execute(
                "INSERT INTO donations (user_id, amount, status, created_at) VALUES (?, ?, ?, ?)",
                (user_id, amount, status, created_at)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Donation.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(id):
        """
        根據 ID 取得單筆捐款紀錄
        :param id: 捐款 ID
        :return: 紀錄字典，或 None
        """
        try:
            conn = get_db_connection()
            donation = conn.execute("SELECT * FROM donations WHERE id = ?", (id,)).fetchone()
            return dict(donation) if donation else None
        except Exception as e:
            print(f"Error in Donation.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_user_id(user_id):
        """
        取得某位特定用戶所有的捐款紀錄
        :param user_id: 用戶 ID
        :return: 捐款紀錄的串列
        """
        try:
            conn = get_db_connection()
            records = conn.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error in Donation.get_by_user_id: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all():
        """
        取得系統內所有的捐款紀錄
        :return: 紀錄串列
        """
        try:
            conn = get_db_connection()
            records = conn.execute("SELECT * FROM donations").fetchall()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error in Donation.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(id, data):
        """
        更新捐款紀錄 (最常見為更新 status)
        :param id: 捐款 ID
        :param data: 包含欲更新欄位 (如 'status') 的資料字典
        :return: 布林值表示成功與否
        """
        try:
            conn = get_db_connection()
            fields = []
            params = []
            
            if 'status' in data:
                fields.append("status = ?")
                params.append(data['status'])
            if 'amount' in data:
                fields.append("amount = ?")
                params.append(data['amount'])

            if not fields:
                return False

            params.append(id)
            query = f"UPDATE donations SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Donation.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(id):
        """
        刪除特定捐款紀錄
        :param id: 紀錄 ID
        :return: 布林值表示成功與否
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM donations WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in Donation.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
