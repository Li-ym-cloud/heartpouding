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


class UserShowDetail(db.Model):
    __tablename__ = 'user_show_detail'

    user_id = db.Column(db.Integer, primary_key=True)
    all_push = db.Column(db.Integer)
    now_push = db.Column(db.Integer)
    up_time = db.Column(db.DateTime)
    history_read = db.Column(db.Integer, default=0)
    read_up_time = db.Column(db.DateTime)
    level = db.Column(db.Integer, default=1)
    all_exper = db.Column(db.Integer, default=100)
    have_exper = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<UserLabel {self.user_id}>'

    def new_level(self):
        self.have_exper += 1
        if self.have_exper >= self.all_exper:
            self.all_exper *= 10
            self.have_exper = 0
            self.level += 1

    def new_level_edit(self):
        self.have_exper += 5
        if self.have_exper >= self.all_exper:
            self.all_exper *= 10
            self.have_exper = 0
            self.level += 1


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
