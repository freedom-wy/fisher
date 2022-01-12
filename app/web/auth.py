from .blueprint import web
from flask import render_template, request, redirect, url_for, flash
from app.forms.register_login_auth import RegisterForm, LoginForm
from app.models.user import User
from app.libs.db_utils import db
from flask_login import login_user, current_user, logout_user


# 根据不同的请求方法判断不同的动作,登录或注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    # 实例化验证器
    register_form = RegisterForm(request.form)
    # 注册
    if request.method == "POST" and register_form.validate():
        with db.auto_commit():
            register_user = User()
            # 保存用户注册的数据
            register_user.set_attrs(register_form.data)
            db.session.add(register_user)
        return redirect(url_for("web.login"))
    return render_template("auth/register.html", form=register_form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("web.index"))
    # 获取post请求表单信息
    login_form = LoginForm(request.form)
    # 登录验证
    if request.method == "POST" and login_form.validate():
        user = User.query.filter_by(email=login_form.email.data).first()
        # 校验密码
        if user and user.check_password(login_form.password.data):
            # 写入cookie信息, 需要在user模型类中继承UserMixin类, 可以在login_user中设置是否记住cookie
            login_user(user, remember=True)
            # 获取get请求信息
            next_url = request.args.get("next")
            if not next_url or not next_url.startswith("/"):
                next_url = url_for("web.index")
            return redirect(next_url)
        else:
            flash("账号不存在或密码错误")
    return render_template("auth/login.html", form=login_form)


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
    logout_user()
    return redirect(url_for("web.index"))
