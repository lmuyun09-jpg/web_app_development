from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
def index():
    """
    進入個人歷史紀錄頁面
    GET: 驗證使用者是否已登入，查出使用者的 History 與 Donation，並渲染 `profile/index.html` 顯示紀錄
    """
    pass
