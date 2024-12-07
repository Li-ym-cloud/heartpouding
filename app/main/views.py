from flask import render_template
from sqlalchemy import func
from ..models import ContentFlushItem, UserLabel
from .. import db
from datetime import datetime, date
from . import main


@main.route('/')
def index():
    today = date.today()
    # 获取今天第一个 ContentFlushItem 的 ID
    first_today_item = ContentFlushItem.query.filter(
        func.date(ContentFlushItem.insert_time) == today,
        ContentFlushItem.content_xinghuo.isnot(None)
    ).order_by(ContentFlushItem.id).first()
    max_context_id = ContentFlushItem.query.order_by(ContentFlushItem.id.desc()).limit(1).first()
    user_label = UserLabel.query.first()
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
        db.session.commit()
    print(last_num)
    return render_template('index.html', content_items=content_items,
                           last_num=last_num)
