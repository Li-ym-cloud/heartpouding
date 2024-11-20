# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 ContentFlush.py
@创建日期 2024/11/6
@描述 文本页面操作类
"""
from flask import Flask, render_template, jsonify, session, redirect, url_for
import PGDBReadWrite as pgrw
from datetime import datetime
from functools import lru_cache

app = Flask(__name__)
app.secret_key = '2411192222'

# 首页显示文本
@app.route('/')
def content_show():
    now = datetime.now()
    record = f"现在是公历{now.year}年{now.month}月{now.day}日，星期{now.strftime('%A')}"
    return render_template('ContentFlush.html', records=record)

# 使用lru缓存存储结果
@lru_cache(maxsize=128)
def get_cached_records(formatted_date, max_id=None):
    if max_id == 0:
        max_id = pgrw.get_read_context(
            f"""select max_content_id 
                from public.user_label 
                where user_id = '000001';"""
        )[0][0]
    records = pgrw.get_read_context(
        f"""select concat('---->', content_xinghuo), id 
            from public.content_flush_item 
            where content_xinghuo is not null  
            and id > {max_id}
            order by id limit 5;"""
    )
    return records

# 获取新的随机文本
@app.route('/refresh_content')
def refresh_content():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')

    # 初始化计数器
    if 'count' not in session:
        session['count'] = 0

    # 获取记录
    records = get_cached_records(formatted_date, session['count'])

    # 更新 max_content_id
    if records:
        max_id = max([record[1] for record in records])
        print(max_id)
        pgrw.update_table(
            f"""update public.user_label 
                 set max_content_id = {max_id} 
                 where user_id = '000001';"""
        )
        session['count'] = max_id

    # 返回记录
    return jsonify({"records": [record[0] for record in records], "count": session['count']})

@app.route('/reset')
def reset():
    session.pop('count', None)
    return redirect(url_for('content_show'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)