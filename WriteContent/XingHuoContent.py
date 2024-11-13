"""
@Author Li
@Email 2308570708@qq.com
@FileName TenApiViewWrite.py
@DateTime 2024/11/13 20:26
@Speak 调用星火模型对爬取的新闻进行二次加工
"""

import requests
import json
import os

Authorization = os.environ.get('Authorization')

if __name__ == '__main__':
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
        "max_tokens": 1406,
        "top_k": 4,
        "temperature": 0.5,
        "messages": [
            {
                "role": "system",
                "content": "你是一个拥有深厚文学素养的新闻工作者,根据提供的一句话和现在的热点，总结出完整的一段总结，字数不能超过150字"
            },
            {
                "role": "user",
                "content": "武汉52岁派出所所长因公牺牲"
            }
        ],
        "model": "4.0Ultra"
    }
    data["stream"] = False
    header = {
        "Authorization": Authorization
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 非流式响应解析示例
    response.encoding = "utf-8"
    for line in response.iter_lines(decode_unicode="utf-8"):
        context_xinghuo = json.loads(line)["choices"][0]["message"]["content"]
        print(context_xinghuo)
