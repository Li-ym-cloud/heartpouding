# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 ContentFlush.py
@创建日期 2024/11/6
@描述 文本页面操作类
"""
from flask import Flask, render_template, jsonify
import PGDBReadWrite as pgrw
from datetime import datetime

app = Flask(__name__)

# 首页显示文本
@app.route('/')
def content_show():
    now = datetime.now()
    record = f"现在是公历{now.year}年{now.month}月{now.day}日，星期{now.strftime('%A')}"
    return render_template('ContentFlush.html', record=record)

# 获取新的随机文本
@app.route('/refresh_content')
def refresh_content():
    record = pgrw.get_read_context(
        "select concat('---->',content_xinghuo) from public.content_flush_item where content is not null order by random() limit 1;"
    )
    return jsonify({"record": record[0]})

if __name__ == '__main__':
    app.run()
