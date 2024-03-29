from flask import Flask
from app.web.blueprint import web
from app.libs.db_utils import db
from app.libs.login_utils import login_manager
from flask_migrate import Migrate
from app.libs.email_utils import mail


def create_app():
    # 实例化FLASK核心对象,通过static_folder指定静态资源路径,指定后,访问最后一个目录,http://192.168.44.148/test2/test.png,通过static_url_path指定访问URL
    # app = Flask(__name__, static_folder="static_pic/test1/test2", static_url_path="/test")
    # template_folder 指定模板文件路径
    app = Flask(__name__)

    # 读取配置文件
    app.config.from_object("app.config")
    app.config.from_object("app.secure_config")

    # 注册蓝图
    app.register_blueprint(web)

    # 注册数据库
    db.init_app(app)
    # with app.app_context():
    # db.create_all(app=app)
    Migrate(app, db)
    # 注册login_manager
    login_manager.init_app(app)
    # 注册mail
    mail.init_app(app)

    return app
