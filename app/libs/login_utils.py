from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()


# 通过login_manager获取用户数据
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
