from .db import get_db_connection
from datetime import datetime
import sqlite3

class User:
    """
    使用者 Model，提供針對 users 表格的完整存取邏輯
    """
    @staticmethod
    def create(username, email, password_hash):
        """
        新增一位使用者
        :param username: 使用者名稱
        :param email: 電子信箱
        :param password_hash: 加密密碼
        :return: 建立成功回傳 id，email 重複或發生錯誤回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, created_at)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            if 'conn' in locals() and conn: conn.rollback()
            return None
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in User.create: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(id):
        """
        根據 ID 取得單筆使用者資料
        :param id: 使用者 ID
        :return: 使用者字典，找不到或發生錯誤回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error in User.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_email(email):
        """
        根據 Email 取得單筆使用者資料 (用於登入檢核)
        :param email: 使用者註冊的 Email
        :return: 使用者字典，找不到或發生錯誤回傳 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error in User.get_by_email: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者列表
        :return: 使用者字典的串列
        """
        try:
            conn = get_db_connection()
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error in User.get_all: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(id, data):
        """
        更新使用者記錄
        :param id: 用戶 ID
        :param data: 欲更新欄位的字典 (支援 username, password_hash)
        :return: 布林值表示成功與否
        """
        try:
            conn = get_db_connection()
            fields = []
            params = []
            
            if 'username' in data:
                fields.append("username = ?")
                params.append(data['username'])
            if 'password_hash' in data:
                fields.append("password_hash = ?")
                params.append(data['password_hash'])

            if not fields:
                return False

            params.append(id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in User.update: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(id):
        """
        刪除使用者記錄
        :param id: 用戶 ID
        :return: 布林值表示成功與否
        """
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            if 'conn' in locals() and conn: conn.rollback()
            print(f"Error in User.delete: {e}")
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
