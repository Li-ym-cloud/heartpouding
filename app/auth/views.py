from datetime import date

from flask import render_template
from sqlalchemy import func
from flask_login import login_user, current_user
from . import auth
from .forms import LoginForm
from ..models import UserPasswordTable, UserLabel, ContentFlushItem
from .. import db


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if current_user.user_id:
            user = UserPasswordTable.query.filter(
                UserPasswordTable.user_id == current_user.user_id
            ).first()
            return render_template('usershow.html', username=user.username)
    except AttributeError as e:
        pass
    form = LoginForm()
    if form.validate_on_submit() and form.registration.data:
        today = date.today()
        print("点击了注册按钮")
        user = UserPasswordTable(
            username=form.username.data,
            password=form.password.data
        )
        user = UserPasswordTable.query.filter_by(username=form.username.data).first()
        if user:
            return render_template('registration.html', form=form, tips="用户名已存在")
        db.session.add(user)
        db.session.commit()
        user_label = UserLabel(
            user_id=UserPasswordTable.query.filter_by(username=form.username.data).first().user_id,
            max_content_id=ContentFlushItem.query.filter(
                func.date(ContentFlushItem.insert_time) == today,
            ).order_by(ContentFlushItem.id).first().id
        )
        db.session.add(user_label)
        db.session.commit()
        login_user(UserPasswordTable.query.filter_by(username=form.username.data).first())
        return render_template('usershow.html', username=form.username.data)
    elif form.validate_on_submit() and form.submit.data:
        print("点击了登录按钮")
        user = UserPasswordTable.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(UserPasswordTable.query.filter_by(username=form.username.data).first())
            return render_template('usershow.html', username=form.username.data)
        else:
            return render_template('registration.html', form=form, tips="账号密码不正确")
    return render_template('registration.html', form=form)
