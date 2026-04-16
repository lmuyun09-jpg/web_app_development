from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁 GET 請求
    渲染首頁模板 `index.html`，若已登入可於前端使用 session['username']
    """
    return render_template('index.html')
