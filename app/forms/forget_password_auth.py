from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired, Email


class ForgetPasswordAuthEmail(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="邮箱不符合规范")])
