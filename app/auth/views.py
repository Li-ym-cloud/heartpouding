from flask import render_template
from . import auth
from .forms import LoginForm
from ..models import UserPasswordTable
from .. import db


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = LoginForm()
    if form.validate_on_submit() and form.registration.data:
        print("点击了注册按钮")
        user = UserPasswordTable(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return render_template('usershow.html', username=form.username.data)
    elif form.validate_on_submit() and form.submit.data:
        print("点击了登录按钮")
        user = UserPasswordTable.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            return render_template('usershow.html', username=form.username.data)
        else:
            return render_template('registration.html', form=form, tips="账号密码不正确")
    return render_template('registration.html', form=form)
