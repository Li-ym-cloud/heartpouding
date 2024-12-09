# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 __init__.py.py
@创建日期 2024/12/9
@描述 
"""
from flask import Blueprint

userShow = Blueprint('userShow', __name__)
from . import views
