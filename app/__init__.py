from flask import Flask
from app.web.book import wb_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.register_blueprint(wb_bp)
    return app
