from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁 GET 請求
    渲染首頁模板 `index.html`，若已登入可加入個人化歡迎詞
    """
    pass
