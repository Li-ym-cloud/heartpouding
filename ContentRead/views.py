from flask import Blueprint, render_template
from .models import ContentFlushItem, db, UserLabel

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    user_label = UserLabel.query.first()
    content_item = ContentFlushItem.query.filter(
        ContentFlushItem.id > user_label.max_content_id,
        ContentFlushItem.content.isnot(None)
    ).first()
    if content_item:
        # 更新UserLabel的max_content_id
        user_label.max_content_id = content_item.id
        db.session.commit()
    return render_template('index.html', content_item=content_item)
