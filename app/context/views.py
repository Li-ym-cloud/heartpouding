# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 views.py
@创建日期 2024/12/9
@描述 
"""
from flask import render_template
from flask_login import current_user

from . import context
from ..models import UserPasswordTable


@context.route('/context', methods=['GET', 'POST'])
def context():
    if current_user.is_authenticated and current_user.user_id:
        user = UserPasswordTable.query.filter(
            UserPasswordTable.user_id == current_user.user_id
        ).first()
        return render_template('usershow.html', username=user.username)
    return render_template('main.index.html')
