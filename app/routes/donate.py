from flask import Blueprint

donate_bp = Blueprint('donate', __name__)

@donate_bp.route('/', methods=['GET'])
def index():
    """
    進入捐香油錢頁面
    GET: 渲染 `donate/index.html`，顯示選擇金額表單與說明
    """
    pass

@donate_bp.route('/pay', methods=['POST'])
def pay():
    """
    提交捐款單
    POST: 接收表單上的捐款金額，建立 Donation 紀錄後模擬付款，狀態設為成功並重導向至 `donate/<id>/success`
    """
    pass

@donate_bp.route('/<int:id>/success', methods=['GET'])
def success(id):
    """
    顯示捐款成功感謝頁
    GET: 撈取指定 Donation 的資料，並渲染 `donate/success.html`
    """
    pass
