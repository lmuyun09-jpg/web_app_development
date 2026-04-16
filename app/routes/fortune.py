from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.fortune import Fortune
from app.models.history import History

fortune_bp = Blueprint('fortune', __name__, url_prefix='/fortune')

@fortune_bp.route('/', methods=['GET'])
def index():
    """
    進入抽籤頁面
    GET: 渲染 `fortune/index.html`，顯示搖籤筒與擲筊的前端介面
    """
    return render_template('fortune/index.html')

@fortune_bp.route('/draw', methods=['POST'])
def draw():
    """
    執行抽籤
    POST: 隨機籤詩，若是會員則寫入紀錄
    """
    # 抽取一首隨機籤詩
    fortune = Fortune.get_random()
    if not fortune:
        flash('抽籤失敗，目前資料庫無籤詩資料，請聯絡管理員', 'danger')
        return redirect(url_for('fortune.index'))

    # 若為會員，存入抽籤紀錄
    if 'user_id' in session:
        History.create({"user_id": session['user_id'], "fortune_id": fortune['id']})

    return redirect(url_for('fortune.result', id=fortune['id']))

@fortune_bp.route('/<int:id>', methods=['GET'])
def result(id):
    """
    顯示籤詩結果
    """
    fortune = Fortune.get_by_id(id)
    if not fortune:
        flash('查無此籤詩紀錄', 'danger')
        return redirect(url_for('fortune.index'))

    return render_template('fortune/result.html', fortune=fortune)
