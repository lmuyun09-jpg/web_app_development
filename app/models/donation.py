from .db import get_db_connection
from datetime import datetime

class Donation:
    @staticmethod
    def create(user_id, amount, status="PENDING"):
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO donations (user_id, amount, status, created_at) VALUES (?, ?, ?, ?)",
            (user_id, amount, status, created_at)
        )
        conn.commit()
        donation_id = cursor.lastrowid
        conn.close()
        return donation_id

    @staticmethod
    def get_by_id(donation_id):
        conn = get_db_connection()
        donation = conn.execute("SELECT * FROM donations WHERE id = ?", (donation_id,)).fetchone()
        conn.close()
        return dict(donation) if donation else None

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        records = conn.execute("SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def update_status(donation_id, status):
        conn = get_db_connection()
        conn.execute("UPDATE donations SET status = ? WHERE id = ?", (status, donation_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = get_db_connection()
        records = conn.execute("SELECT * FROM donations").fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def delete(donation_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM donations WHERE id = ?", (donation_id,))
        conn.commit()
        conn.close()
        return True
