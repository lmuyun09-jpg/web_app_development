from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
fortune_bp = Blueprint('fortune', __name__, url_prefix='/fortune')
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
donate_bp = Blueprint('donate', __name__, url_prefix='/donate')

def init_app(app):
    from .main import main_bp
    from .auth import auth_bp
    from .fortune import fortune_bp
    from .profile import profile_bp
    from .donate import donate_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fortune_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(donate_bp)
