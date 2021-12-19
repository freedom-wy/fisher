from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange


class searchArgsVerification(Form):
    """
    搜索参数校验
    """
    # 搜索关键字长度
    q = StringField(validators=[Length(min=1, max=30)])
    # 页码
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)