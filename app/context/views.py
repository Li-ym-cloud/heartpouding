from datetime import date

from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from . import context
from .forms import EditForm
from ..models import UserPasswordTable, ContentFlushItem, UserShowDetail
from .. import db


@context.route('/context', methods=['GET', 'POST'])
def context():
    if not current_user.is_authenticated or not current_user.user_id:
        return redirect(url_for('main.index'))  # 或者其他适当的重定向路径

    user = UserPasswordTable.query.filter(
        UserPasswordTable.user_id == current_user.user_id
    ).first()

    form = EditForm()
    today = date.today()
    if form.validate_on_submit():
        new_context = ContentFlushItem(
            content=form.body.data,
            content_xinghuo=form.body.data,
            context_author=current_user.user_id
        )
        db.session.add(new_context)
        try:
            db.session.commit()
            user_num = UserShowDetail.query.filter(
                UserShowDetail.user_id == current_user.user_id
            ).first()
            if user_num:
                user_num.all_push += 1
                user_num.now_push += 1
                user_num.up_time = today
            elif user_num and user.all_push is None:
                user_num.all_push += 1
                user_num.now_push += 1
                user_num.up_time = today
            else:
                up_user_num = UserShowDetail(
                    user_id=current_user.user_id,
                    all_push=1,
                    now_push=1,
                    up_time=today
                )
                db.session.add(up_user_num)
            db.session.commit()
            flash('发布成功', 'success')  # 使用 flash 显示成功消息
            form = EditForm()  # 创建一个新的表单实例来清空表单
        except Exception as e:
            db.session.rollback()
            flash(f'发布失败: {str(e)}', 'danger')  # 发生错误时显示错误消息

        return redirect(url_for('context.context'))  # 重定向以避免重复提交问题
    user_num = UserShowDetail.query.filter(
        UserShowDetail.user_id == current_user.user_id
    ).first()
    return render_template('usershow.html', username=user.username, form=form, user_num=user_num)
