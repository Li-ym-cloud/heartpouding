# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 __init__.py.py
@创建日期 2024/11/6
@描述 
"""
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
db = SQLAlchemy()
login_manager = LoginManager()
pagadown = PageDown()
login_manager.login_view = 'auth.registration'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap = Bootstrap(app)
    pagadown.init_app(app) # 富文本
    from .main import main as main_blueprint  # 导入蓝图
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .userShow import userShow as userShow_blueprint
    app.register_blueprint(userShow_blueprint, url_prefix='/usershow')
    from .context import context as context_blueprint
    app.register_blueprint(context_blueprint, url_prefix='/context')
    with app.app_context():
        db.create_all()
    return app
