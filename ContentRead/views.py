from flask import Blueprint, render_template
from sqlalchemy import func
from .models import ContentFlushItem, db, UserLabel
from datetime import datetime, date

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    today = date.today()
    # 获取今天第一个 ContentFlushItem 的 ID
    first_today_item = ContentFlushItem.query.filter(
        func.date(ContentFlushItem.insert_time) == today,
        ContentFlushItem.content.isnot(None)
    ).order_by(ContentFlushItem.id).first()
    user_label = UserLabel.query.first()
    if first_today_item and first_today_item.id > user_label.max_content_id:
        # 更新UserLabel的max_content_id为当前日期的最新id
        user_label.max_content_id = first_today_item.id
        db.session.commit()
    # 假设你想获取最新的5条记录，这里使用了降序排列
    content_items = ContentFlushItem.query.filter(
        ContentFlushItem.id > user_label.max_content_id,
        ContentFlushItem.content.isnot(None),
        db.func.length(ContentFlushItem.content) > 5
    ).order_by(ContentFlushItem.id.asc()).limit(3).all()

    if content_items:
        # 更新UserLabel的max_content_id为最新获取到的内容项中的最大ID
        max_id = max(item.id for item in content_items)
        user_label.max_content_id = max_id
        db.session.commit()

    return render_template('index.html', content_items=content_items)
