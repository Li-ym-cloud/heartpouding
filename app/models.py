from . import db, login_manager
from flask_login import UserMixin


class ContentFlushItem(db.Model):
    __tablename__ = 'content_flush_item'

    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    content = db.Column(db.Text, nullable=True)
    flush_sec = db.Column(db.Integer, db.Computed("length(content)"), nullable=True)
    content_xinghuo = db.Column(db.Text, nullable=True)
    context_author = db.Column(db.Integer)

    def __repr__(self):
        return f'<ContentFlushItem {self.id}>'


class UserLabel(db.Model):
    __tablename__ = 'user_label'

    user_id = db.Column(db.Integer, primary_key=True)
    max_content_id = db.Column(db.BigInteger, nullable=True)
    label_one = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<UserLabel {self.user_id}>'


class UserPasswordTable(UserMixin, db.Model):
    __tablename__ = "user_password_table"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)

    def __repr__(self):
        return f'<UserPasswordTable {self.user_id}>'

    def get_id(self):
        return str(self.user_id)  # 返回字符串类型的 user_id

    @login_manager.user_loader
    def load_user(user_id):
        return UserPasswordTable.query.get(int(user_id))
