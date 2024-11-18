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
from functools import lru_cache

app = Flask(__name__)


# 首页显示文本
@app.route('/')
def content_show():
    now = datetime.now()
    record = f"现在是公历{now.year}年{now.month}月{now.day}日，星期{now.strftime('%A')}"
    return render_template('ContentFlush.html', records=record)


# 使用lru缓存存储结果
@lru_cache(maxsize=128)
def get_cached_records(formatted_date):
    records = pgrw.get_read_context(
        f"""select concat('---->',content_xinghuo) 
            from public.content_flush_item 
            where content_xinghuo is not null  
            and insert_time::date = '{formatted_date}'::date
            order by random() limit 20;"""
    )
    return [record[0] for record in records]


# 获取新的随机文本
@app.route('/refresh_content')
def refresh_content():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    records = get_cached_records(formatted_date)
    return jsonify({"records": records})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
