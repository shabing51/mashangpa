from curl_cffi import requests
# import subprocess
import execjs

with open('./js/match2.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(source=js_code)

headers = {
    "referer": "https://match.yuanrenxue.cn/match/2",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "qcngxf1p24fbthxucr94o1std0qhdms8",
}
session = requests.Session(headers=headers, cookies=cookies)

url = "https://match.yuanrenxue.cn/api/question/2"

total = 0

for page_num in range(1, 6, 1):
    params = {
        "page": str(page_num),
        "pageSize": "10",
        "kw": ""
    }
    if page_num == 5:
        session.headers.update({"user-agent": "yuanrenxue"})
    session.cookies.update({'m': ctx.call('m')})
    response = session.get(url, params=params)
    data = response.json()['data']
    print(f"第{page_num}页数据: {data}")
    total += sum(data)

print(total)