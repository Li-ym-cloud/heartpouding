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
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bootstrap = Bootstrap(app)
    from .views import bp  # 导入蓝图
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app

from . import views
from . import models

