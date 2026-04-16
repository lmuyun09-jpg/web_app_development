from flask import Blueprint

fortune_bp = Blueprint('fortune', __name__)

@fortune_bp.route('/', methods=['GET'])
def index():
    """
    進入抽籤頁面
    GET: 渲染 `fortune/index.html`，顯示搖籤筒與擲筊的前端介面
    """
    pass

@fortune_bp.route('/draw', methods=['POST'])
def draw():
    """
    執行抽籤
    POST: 呼叫 Model 產生隨機籤詩，若為登入會員則儲存至 History，處理後重導向至 `fortune/<id>`
    """
    pass

@fortune_bp.route('/<int:id>', methods=['GET'])
def result(id):
    """
    顯示籤詩結果
    GET: 藉由傳入的 history id 或是 fortune id 查出籤詩結果，並渲染 `fortune/result.html` 分享解讀
    """
    pass
