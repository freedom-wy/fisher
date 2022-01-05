from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱不符合规范")])
    password = PasswordField(validators=[DataRequired(message="密码不可以为空"), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="昵称至少需要两个字符,最多10个字符")])

    # 自定义验证器
    def validate_email(self, field):
        """
        查询数据库中是否有相同的email
        :param field:
        :return:
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("改昵称已存在")
