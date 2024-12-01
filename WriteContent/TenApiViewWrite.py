"""
@Author Li
@Email 2308570708@qq.com
@FileName TenApiViewWrite.py
@DateTime 2024/11/920:26
@Speak 通过https://docs.tenapi.cn/获得数据，本api预估在241224停止更新 --已经废弃
"""

import PGDBReadWrite as pgrw
import requests
import XingHuoContent as xhc


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


"""
这部分代码已经因为api失效而过期--2024年11月30日
改用https://orz.ai/dailynews/?platform=
hot_list = [
    "https://tenapi.cn/v2/toutiaohotnew",
    "https://tenapi.cn/v2/baiduhot",
    "https://tenapi.cn/v2/douyinhot",
    "https://tenapi.cn/v2/weibohot",
    "https://tenapi.cn/v2/zhihuhot",
    "https://tenapi.cn/v2/bilihot",
    "https://tenapi.cn/v2/toutiaohot"
]
for hot_url in hot_list:
    time.sleep(10)
    print(f"开始录入网址{hot_url}的数据")
    context_0_list = hot_view(hot_url, "data.name")
    if context_0_list is not None:
        context_list = [{"content": item_c, "content_xinghuo": xhc.return_context_xinghuo(item_c)} for item_c in
                        context_0_list]
        pgrw.write_context(context_list, ["content", "content_xinghuo"])
    context_music_0_list = music_com("https://tenapi.cn/v2/comment")
    if context_music_0_list is not None:
        context_list = [{"content": item_c, "content_xinghuo": xhc.return_context_xinghuo(item_c)} for item_c in
                        context_music_0_list]
        pgrw.write_context(context_list, ["content", "content_xinghuo"])
"""


@error_handler
def orz_com(api_url):
    response = requests.get(api_url)
    context_list = []
    if response.status_code == 200:
        json_data = response.json()['data']
        for title_and_desc in json_data:
            if str(title_and_desc['desc']).strip() == "" or title_and_desc['desc'] is None:
                print(f"{title_and_desc['title']}----需要进入大模型部分")
                context_list.append({"content": title_and_desc['title'],
                                     "content_xinghuo": xhc.return_context_xinghuo(title_and_desc['title'])})
            elif len(str(title_and_desc['desc'])) < 3 and len(str(title_and_desc['title'])) < 3:
                pass
            else:
                context_list.append({"content": title_and_desc['title'],
                                     "content_xinghuo": title_and_desc['desc']})
    return context_list


site_names = ["baidu", "shaoshupai", "weibo", "zhihu", "36kr", "52pojie", "bilibili", "douban", "hupu", "tieba",
              "juejin", "douyin", "v2ex", "jinritoutiao"]
https_bfe = "https://orz.ai/dailynews/?platform="
for site_name in site_names:
    api_url = https_bfe + site_name
    print(f"此刻输出的link为{api_url}")
    context_list = orz_com(api_url)
    if len(context_list) <= 0:
        pass
    else:
        print(f"本次输出条数为{len(context_list)}")
        pgrw.write_context(context_list, ["content", "content_xinghuo"])
