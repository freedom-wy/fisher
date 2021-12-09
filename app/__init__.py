from flask import Flask
from app.web.blue_print import book_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.register_blueprint(book_bp)
    return app
