from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired,len(5,30)])
    password = PasswordField('用户密码',validators=[DataRequired])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')