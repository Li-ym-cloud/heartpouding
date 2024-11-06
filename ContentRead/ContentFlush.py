# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 ContentFlush.py
@创建日期 2024/11/6
@描述 
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('ContentFlush.html')


if __name__ == '__main__':
    app.run()
