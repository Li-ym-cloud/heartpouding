# !usr/bin/env python
# coding=utf-8

"""
@作者: LiShuangJiang
@文件名 PGDBReadWrite.py
@创建日期 2024/11/6
@描述 postgresql的操作类
"""
import psycopg2
import os

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn


def get_read_context(sql_txt):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql_txt)
    record = cur.fetchone()
    cur.close()
    conn.close()
    if record is None:
        return None
    else:
        return record


def write_context(context_list):
    if context_list is None or len(context_list)==0:
        print(f"提交事务成功失败，暂无数据")
        return
    conn = get_db_connection()
    cur = conn.cursor()
    # 使用executemany来插入多条数据
    # 首先构造一个包含占位符的SQL语句
    query = """
    INSERT INTO public.content_flush_item ("content")
    VALUES (%s);
    """
    # 然后将contextlist中的每个元素作为一个元组传递给executemany
    cur.executemany(query, [(context,) for context in context_list])
    # 提交事务
    conn.commit()
    print(f"提交事务成功{len(context_list)}")
    cur.close()
    conn.close()
