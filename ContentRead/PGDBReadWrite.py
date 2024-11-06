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
