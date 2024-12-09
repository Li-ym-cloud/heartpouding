from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, ValidationError
from ..models import UserPasswordTable


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), length(5, 30)])
    password = PasswordField('用户密码', validators=[DataRequired(), length(5, 30)])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')
    registration = SubmitField('注册')

    def validate_username(self, field):
        if UserPasswordTable.query.filter_by(username=field.data).first():
            raise ValidationError('Username aleady in use!!!')
