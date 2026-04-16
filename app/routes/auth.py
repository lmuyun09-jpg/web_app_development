from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理註冊功能
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 基本驗證
        if not username or not email or not password:
            flash('所有欄位(名稱、信箱、密碼) 皆為必填', 'danger')
            return redirect(url_for('auth.register'))

        # 寫入 Model
        password_hash = generate_password_hash(password)
        user_id = User.create(username, email, password_hash)

        if user_id:
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗：Email 可能已被使用，請更換並重試', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理登入功能
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 基本驗證
        if not email or not password:
            flash('信箱與密碼皆為必填', 'danger')
            return redirect(url_for('auth.login'))

        # 檢核使用者
        user = User.get_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('登入失敗：信箱或密碼錯誤', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理登出功能
    """
    session.clear()
    flash('您已成功登出', 'info')
    return redirect(url_for('main.index'))
