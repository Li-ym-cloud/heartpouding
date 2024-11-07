# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 ContentFlush.py
@创建日期 2024/11/6
@描述 文本页面操作类
"""
from flask import Flask, render_template
import PGDBReadWrite as pgrw

app = Flask(__name__)


@app.route('/')
def content_show():
    record = pgrw.get_read_context("select content from public.content_flush_item order by random() limit 1;")
    return render_template('ContentFlush.html', record=record[0])


if __name__ == '__main__':
    app.run()
