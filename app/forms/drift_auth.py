from wtforms import Form, StringField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class DriftForm(Form):
    """
    向他请求此书后页面post请求的验证
    """
    # 收件人姓名
    recipient_name = StringField(validators=[DataRequired(), Length(
        min=2, max=20, message="收件人姓名长度必须在2到20个字符之间")])
    # 手机号
    mobile = StringField(validators=[DataRequired(), Regexp("^1[0-9]{10}$", 0, "请输入正确的手机号码")])
    # 留言信息
    message = StringField()
    # 收件地址
    address = StringField(validators=[DataRequired(), Length(min=10, max=70, message="收件人地址必须在2到80个字符之间")])

