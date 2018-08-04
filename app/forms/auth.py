from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError

from app.models.user import User


class LoginForms(Form):
    nickname = StringField(validators=[DataRequired(message="昵称不能为空"), Length(min=2, max=10, message="至少需要2个字符，最多10个字符")])
    password = PasswordField(validators=[DataRequired(message="请输入密码"), Length(min=6, max=32, message="至少需要6个字符，最多32个字符")])


class MyEmailForms(Form):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
                                            Email(message='电子邮箱不符合规范')])


class RegisterForms(LoginForms, MyEmailForms):
    pass
    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError("电子邮箱已存在")
