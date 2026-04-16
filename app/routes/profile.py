from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.history import History
from app.models.donation import Donation

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def index():
    """
    進入個人歷史紀錄頁面
    """
    if 'user_id' not in session:
        flash('請先登入後才能檢視歷史紀錄', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    # 向 Model 拿取歷史紀錄與香油錢紀錄
    histories = History.get_by_user_id(user_id)
    donations = Donation.get_by_user_id(user_id)

    return render_template('profile/index.html', histories=histories, donations=donations)
