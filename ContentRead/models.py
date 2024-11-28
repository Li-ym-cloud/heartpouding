from ContentRead import db


class ContentFlushItem(db.Model):
    __tablename__ = 'content_flush_item'

    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    content = db.Column(db.Text, nullable=True)
    flush_sec = db.Column(db.Integer, nullable=True)  # 由于是计算列，这里不设置默认值
    content_xinghuo = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ContentFlushItem {self.id}>'