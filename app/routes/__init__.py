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
