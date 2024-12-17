"""
目前这里使用的还是基于日走的逻辑，每个用户默认只展示当天最新的数据，而不展示过去日期的数据
"""
from flask import render_template
from sqlalchemy import func
from flask_login import current_user
from ..models import ContentFlushItem, UserLabel, UserShowDetail
from .. import db
from datetime import datetime, date
from . import main


@main.route('/')
def index():
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    # 获取今天第一个 ContentFlushItem 的 ID
    first_today_item = ContentFlushItem.query.filter(
        func.date(ContentFlushItem.insert_time) == today,
        ContentFlushItem.content_xinghuo.isnot(None)
    ).order_by(ContentFlushItem.id).first()
    max_context_id = ContentFlushItem.query.order_by(ContentFlushItem.id.desc()).limit(1).first()
    if current_user.is_authenticated and current_user.user_id:
        user_label = UserLabel.query.filter(
            UserLabel.user_id == current_user.user_id
        ).first()
        if first_today_item and first_today_item.id > user_label.max_content_id:
            # 更新UserLabel的max_content_id为当前日期的最新id
            user_label.max_content_id = first_today_item.id
            db.session.commit()
        # 假设你想获取最新的1条记录，这里使用了降序排列
        content_items = ContentFlushItem.query.filter(
            ContentFlushItem.id > user_label.max_content_id,
            ContentFlushItem.content_xinghuo.isnot(None),
            db.func.length(ContentFlushItem.content_xinghuo) > 5
        ).order_by(ContentFlushItem.id.asc()).limit(1).all()
        if content_items:
            # 更新UserLabel的max_content_id为最新获取到的内容项中的最大ID
            max_id = max(item.id for item in content_items)
            last_num = max_context_id.id - max_id
            user_label.max_content_id = max_id
            user_num = UserShowDetail.query.filter(
                UserShowDetail.user_id == current_user.user_id
            ).first()
            if user_num and user_num.history_read is None:
                user_num.history_read = 1
                user_num.new_level()
                user_num.read_up_time = today
            elif user_num and user_num.history_read is not None:
                user_num.history_read += 1
                user_num.new_level()
                user_num.read_up_time = today
            else:
                up_user_num = UserShowDetail(
                    user_id=current_user.user_id,
                    history_read=1,
                    all_push=0,
                    now_push=0,
                    read_up_time=today
                )
                db.session.add(up_user_num)
            db.session.commit()
            return render_template('index.html', content_items=content_items,
                                   last_num=last_num)
    else:
        # 随机获得一条
        content_items = ContentFlushItem.query.filter(
            ContentFlushItem.content_xinghuo.isnot(None),
            func.date(ContentFlushItem.insert_time) >= first_day_of_month,  # 本月开始时间
            func.date(ContentFlushItem.insert_time) <= today,  # 本月结束时间
            db.func.length(ContentFlushItem.content_xinghuo) > 5
        ).order_by(db.func.random()).limit(1).all()
        return render_template('index.html', content_items=content_items,
                               last_num=9999)
