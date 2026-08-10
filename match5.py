import execjs
from curl_cffi import requests

with open('./js/match5.js', "r", encoding='utf-8') as fr:
    js_code = fr.read()
ctx = execjs.compile(js_code)

headers = {
    "referer": "https://match.yuanrenxue.cn/match/5",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "qcngxf1p24fbthxucr94o1std0qhdms8",
}
session = requests.Session(headers=headers, cookies=cookies)


url = "https://match.yuanrenxue.cn/api/question/5"

call_res = ctx.call('shabing', 2)

session.cookies.update({
    "m": call_res["cookie_m"],
    "RM4hZBv0dDon443M": call_res["RM4"]
})
params = call_res['params']
print(params)
resp = session.get(url, params=params)
print(resp.url)

print(resp.json())



