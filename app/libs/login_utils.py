from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = "web.login"
login_manager.login_message = "请先登录或注册"


# 通过login_manager获取用户数据,这里完全不知道是为啥。。
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
