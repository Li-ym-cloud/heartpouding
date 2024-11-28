from flask import Blueprint, render_template
from .models import ContentFlushItem,db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    content_item = ContentFlushItem.query.filter(ContentFlushItem.content.isnot(None)).order_by(db.func.random()).first()
    return render_template('index.html', content_item=content_item)
