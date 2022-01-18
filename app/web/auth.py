from .blueprint import web
from flask import render_template, request, redirect, url_for, flash
from app.forms.register_login_auth import RegisterForm, LoginForm
from app.models.user import User
from app.libs.db_utils import db
from flask_login import login_user, current_user, logout_user
from app.forms.forget_password_auth import ForgetPasswordAuthEmail, ResetPasswordForm
from app.libs.email_utils import handle_send_mail


# 根据不同的请求方法判断不同的动作,登录或注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册,传入昵称,邮箱,密码
    :return:
    """
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
    """
    1、检查邮箱是否符合要求
    2、通过邮箱查询用户
    :return:
    """
    forget_password_form = ForgetPasswordAuthEmail(request.form)
    if request.method == "POST" and forget_password_form.validate():
        # 通过邮箱查用户,返回用户数据或404
        user = User.query.filter_by(email=forget_password_form.email.data).first_or_404()
        # 解决循环引用
        handle_send_mail(to=user.email, subject="重置你的密码", template="email/reset_password.html", user=user,
                         token=user.generate_token())
        flash("密码重置邮件已发送至{},该邮件5分钟过期".format(user.email))
    return render_template("auth/forget_password_request.html", form=forget_password_form)


# 该视图可以随便进入,即为路径后token数据随便写
@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    password_form = ResetPasswordForm(request.form)
    if request.method == "POST" and password_form.validate():
        # 重置密码
        success = User.reset_password(token, password_form.password1.data)
        if success:
            flash("密码更新成功， 请使用新密码登录")
            return redirect(url_for("web.login"))
        else:
            flash("密码重置失败")
            return redirect(url_for("web.forget_password_request"))
    return render_template("auth/forget_password.html", form=password_form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("web.index"))
