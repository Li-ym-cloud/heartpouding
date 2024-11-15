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


def write_context(context_list, col_names):
    if not context_list:
        print("提交事务失败，暂无数据")
        return

    # 假设get_db_connection是获取数据库连接的方法
    conn = get_db_connection()
    cur = conn.cursor()

    # 构造字段名部分
    fields = ', '.join([f'"{col}"' for col in col_names])
    # 构造占位符部分
    placeholders = ', '.join(['%s'] * len(col_names))

    # 构造完整的SQL语句
    query = f"""
    INSERT INTO public.content_flush_item ({fields})
    VALUES ({placeholders});
    """

    # 将context_list中的每个元素转换成元组列表，每个元组对应一行记录
    data_to_insert = [tuple(context[col] for col in col_names) for context in context_list]

    try:
        # 执行插入操作
        cur.executemany(query, data_to_insert)
        # 提交事务
        conn.commit()
        print(f"涉及{', '.join(col_names)}的事务，提交事务成功{len(context_list)}条记录")
    except Exception as e:
        print(f"提交事务失败: {e}")
        # 如果发生错误，回滚事务
        conn.rollback()
    finally:
        # 关闭游标和连接
        cur.close()
        conn.close()
