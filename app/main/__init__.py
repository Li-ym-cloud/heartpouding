from flask import Blueprint

main = Blueprint('main', __name__)
# 末尾导入，避免循环引用
from . import views, errors
