from .blueprint import web
from flask import render_template, request
from app.forms.register_login_auth import RegisterForm
from app.models.user import User


# 根据不同的请求方法判断不同的动作,登录或注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    # 实例化验证器
    register_form = RegisterForm(request.form)
    # 注册
    if request.method == "POST" and register_form.validate():
        register_user = User()
        # 保存用户注册的数据
        register_user.set_attrs(register_form.data)
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
