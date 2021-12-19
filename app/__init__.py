from flask import Flask
from .web.blueprint import book_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.register_blueprint(book_bp)
    return app
