from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, EqualTo


class ForgetPasswordAuthEmail(Form):
    """
    重置密码时填写的email
    """
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱不符合规范")])


class ResetPasswordForm(Form):
    """
    用于校验重置密码时的密码和新密码,EqualTo
    """
    # 新密码
    password1 = PasswordField(validators=[DataRequired(), Length(
        6, 32, message="密码长度至少需要在6到20个字符之间"), EqualTo(
        "password2", message="两次输入的密码不相同")])
    # 确认密码
    password2 = PasswordField(validators=[DataRequired(), Length(
        6, 32, message="密码长度至少需要在6到20个字符之间")])
