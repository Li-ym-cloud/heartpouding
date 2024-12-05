"""
@Author Li
@Email 2308570708@qq.com
@FileName TenApiViewWrite.py
@DateTime 2024/11/13 20:26
@Speak 调用星火模型对爬取的新闻进行二次加工
"""
import time

import requests
import json
import os

from psycopg2 import connect

Authorization = os.environ.get('Authorization')


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
            # 可以选择在这里记录错误或进行其他处理
    return wrapper


@error_handler
def return_context_xinghuo(context: str):
    time.sleep(1)
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
        "max_tokens": 1406,
        "top_k": 4,
        "temperature": 0.5,
        "messages": [
            {
                "role": "system",
                "content": """"你是一个严谨的数据分析专家,请根据我提供的一句话，结合时下热点，判断对热点所属的行业造成的影响，要求字数不超过150字，只罗列一条分析，要有历史依据，输出格式为\n\"\n所属行业:\n起因:\n热分析结果:\n佐证:\n\""""
            },
            {
                "role": "user",
                "content": context
            }
        ],
        "model": "4.0Ultra"
    }
    data["stream"] = False
    header = {
        "Authorization": Authorization
    }
    response = requests.post(url, headers=header, json=data, stream=True)
    response.encoding = "utf-8"
    for line in response.iter_lines(decode_unicode="utf-8"):
        print(line)
        context_xinghuo = json.loads(line)["choices"][0]["message"]["content"]
        return context_xinghuo
