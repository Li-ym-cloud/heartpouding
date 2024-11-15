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
                "content": "你是一个拥有深厚文学素养的文字工作者,根据提供的一句话和现在的热点，总结出完整的一段总结，字数不能超过150字，不出现含糊信息，不要出现X字样，不要出现新闻工作者字样"
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
        context_xinghuo = json.loads(line)["choices"][0]["message"]["content"]
        return context_xinghuo
