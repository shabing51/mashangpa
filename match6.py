from curl_cffi import requests
import execjs
from loguru import logger

with open('./js/match6.js', 'r', encoding='utf8') as fr:
    js_code = fr.read()
ctx = execjs.compile(js_code)

headers = {
    "referer": "https://match.yuanrenxue.cn/match/6",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "1i5v0k8r6a43wlsyiawqngaitay2n0xi",
}
session = requests.Session(headers=headers, cookies=cookies)

url = "https://match.yuanrenxue.cn/api/question/6"

total = 0
for page_num in range(1,6,1):
    params = ctx.call('getParams', page_num)
    # print(params)
    response = session.get(url, params=params)
    data = response.json()['data']
    logger.info(f"第{page_num}页数据: {data}")
    total += sum(data)

print(f"Total is {total}")