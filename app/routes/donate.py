from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.donation import Donation

donate_bp = Blueprint('donate', __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
def index():
    """
    進入捐香油錢頁面
    """
    return render_template('donate/index.html')

@donate_bp.route('/pay', methods=['POST'])
def pay():
    """
    提交捐款單並模擬付款
    """
    amount = request.form.get('amount')
    
    if not amount or not amount.isdigit() or int(amount) <= 0:
        flash('請輸入大於 0 的正確金額', 'danger')
        return redirect(url_for('donate.index'))

    # 使用者可能為訪客，此時 user_id 為 None
    user_id = session.get('user_id')
    
    donation_id = Donation.create({'user_id': user_id, 'amount': int(amount), 'status': 'SUCCESS'})
    
    if donation_id:
        return redirect(url_for('donate.success', id=donation_id))
    else:
        flash('紀錄建立失敗，請稍後重試', 'danger')
        return redirect(url_for('donate.index'))

@donate_bp.route('/<int:id>/success', methods=['GET'])
def success(id):
    """
    顯示捐款成功感謝頁
    """
    donation = Donation.get_by_id(id)
    if not donation:
        flash('查無此捐款紀錄', 'danger')
        return redirect(url_for('donate.index'))
        
    return render_template('donate/success.html', donation=donation)
