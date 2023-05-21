# 核心对象初始化
from flask import Flask
from apps.web.book import web


def create_app():
    app = Flask(__name__)
    app.config.from_object("apps.config")
    register_blueprint(app)
    return app


def register_blueprint(app):
    from apps.web.blueprint import web
    app.register_blueprint(web)
