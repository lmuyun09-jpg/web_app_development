import os
from flask import Flask
from dotenv import load_dotenv

def create_app(test_config=None):
    # 載入環境變數
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from .routes import init_app
    init_app(app)

    return app
