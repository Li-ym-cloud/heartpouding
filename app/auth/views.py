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
        return render_template('registration.html', form=form)
    return render_template('registration.html', form=form)
