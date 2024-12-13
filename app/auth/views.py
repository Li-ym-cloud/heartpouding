from datetime import date

from flask import render_template, url_for
from sqlalchemy import func
from flask_login import login_user, current_user
from werkzeug.utils import redirect

from . import auth
from .forms import LoginForm
from ..context.forms import EditForm
from ..models import UserPasswordTable, UserLabel, ContentFlushItem, UserShowDetail
from .. import db


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form_show = EditForm()
    if current_user.is_authenticated and current_user.user_id:
        return redirect(url_for('context.context'))
    form = LoginForm()
    if form.validate_on_submit() and form.registration.data:
        today = date.today()
        print("点击了注册按钮")
        user = UserPasswordTable(
            username=form.username.data,
            password=form.password.data
        )
        user_have = UserPasswordTable.query.filter_by(username=form.username.data).first()
        if user_have:
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
        up_user_num = UserShowDetail(
            user_id=UserPasswordTable.query.filter_by(username=form.username.data).first().user_id,
            history_read=0,
            all_push=0,
            now_push=0,
            up_time=today,
            read_up_time=today
        )
        db.session.add(up_user_num)
        db.session.commit()
        login_user(UserPasswordTable.query.filter_by(username=form.username.data).first())
        return redirect(url_for('context.context'))
    elif form.validate_on_submit() and form.submit.data:
        print("点击了登录按钮")
        user = UserPasswordTable.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(UserPasswordTable.query.filter_by(username=form.username.data).first())
            today = date.today()
            user_num = UserShowDetail.query.filter(
                UserShowDetail.user_id == current_user.user_id,
                func.date(UserShowDetail.up_time) == today,
            ).first()
            user_num_noday = UserShowDetail.query.filter(
                UserShowDetail.user_id == current_user.user_id
            ).first()
            if user_num:
                print("---------------------")
                user_num.now_push = 0
                user_num.up_time = today
            elif user_num_noday is None:
                up_user_num = UserShowDetail(
                    user_id=current_user.user_id,
                    history_read=0,
                    all_push=0,
                    now_push=0,
                    up_time=today,
                    read_up_time=today
                )
                db.session.add(up_user_num)
            else:
                pass
            db.session.commit()
            return redirect(url_for('context.context'))
        else:
            return render_template('registration.html', form=form, tips="账号密码不正确")
    return render_template('registration.html', form=form)
