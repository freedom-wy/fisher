from .blueprint import web
from flask import render_template


# 根据不同的请求方法判断不同的动作,登录或注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("auth/register.html", form={"data": {}})


@web.route('/login', methods=['GET', 'POST'])
def login():
    pass


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    pass
