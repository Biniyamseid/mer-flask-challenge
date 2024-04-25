from flask import Flask
from .config import DevelopmentConfig,TestingConfig

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    from .routes.book_routes import book_bp
    app.register_blueprint(book_bp)

    return app
