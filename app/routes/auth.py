from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理註冊功能
    GET: 渲染 `auth/register.html` 表單
    POST: 接收表單資訊、驗證資料、建立 User，成功後重導向 `/auth/login`
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理登入功能
    GET: 渲染 `auth/login.html` 表單
    POST: 接收帳密、驗證身份，成功寫入 session 並重導向首頁，失敗則回傳錯誤訊息
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理登出功能
    GET: 清除 session 中的使用者資訊，然後重導向首頁
    """
    pass
