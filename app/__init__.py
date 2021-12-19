from flask import Flask
from .web.blueprint import book_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")
    app.config.from_object("app.secure_config")
    app.register_blueprint(book_bp)
    return app
