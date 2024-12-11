from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, length


class EditForm(FlaskForm):
    body = PageDownField("发布消息", validators=[DataRequired(), length(10, 100)])
    submit = SubmitField('提交')
