"""
@Author Li
@Email 2308570708@qq.com
@FileName TenApiViewWrite.py
@DateTime 2024/11/920:26
@Speak 通过https://docs.tenapi.cn/获得数据，本api预估在241224停止更新
"""
from ContentRead import PGDBReadWrite as pgrw
import requests
import time

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
            # 可以选择在这里记录错误或进行其他处理
    return wrapper

@error_handler
def hot_view(api_url, key=None):
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
        context_list = [data_item[key.split('.')[1]] for data_item in json_data[key.split('.')[0]]]
        return context_list
    else:
        return None

@error_handler
def music_com(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()['data']
        return [f"{json_data['songs']}' '{json_data['sings']}' '{json_data['comment']}"]
    else:
        return None


hot_list = [
    "https://tenapi.cn/v2/baiduhot",
    "https://tenapi.cn/v2/douyinhot",
    "https://tenapi.cn/v2/weibohot",
    "https://tenapi.cn/v2/zhihuhot",
    "https://tenapi.cn/v2/bilihot",
    "https://tenapi.cn/v2/toutiaohot",
    "https://tenapi.cn/v2/toutiaohotnew"
]
for hot_url in hot_list:
    time.sleep(10)
    print(f"开始录入网址{hot_url}的数据")
    context_list = hot_view(hot_url, "data.name")
    pgrw.write_context(context_list)
    context_music_list = music_com("https://tenapi.cn/v2/comment")
    pgrw.write_context(context_music_list)
