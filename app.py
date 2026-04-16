from app import create_app
from app.models.db import init_db

app = create_app()

if __name__ == '__main__':
    # 啟動時自動初始化資料庫結構
    with app.app_context():
        init_db()
    app.run(debug=True)
