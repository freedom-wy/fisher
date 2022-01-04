from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱不符合规范")])
    password = PasswordField(validators=[DataRequired(message="密码不可以为空"), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称至少需要两个字符,最多10个字符")])
