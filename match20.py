from curl_cffi import requests
import time
import hashlib  

def sign(page_num, t, salt:str='D#uqGdcw41pWeNXm'):
    return hashlib.md5(
        f"{page_num}|{t}{salt}".encode()
    ).hexdigest()

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": "https://match.yuanrenxue.cn/match/20",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "1i5v0k8r6a43wlsyiawqngaitay2n0xi",
}
session = requests.Session(headers=headers, cookies=cookies)


url = "https://match.yuanrenxue.cn/api/question/20"

total = 0
for page_num in range(1,6):
    t = int(time.time()*1000)
    params = {
        "sign": sign(page_num, t),
        "t": str(t),
        "page": str(page_num)
    }
    response = session.get(url, params=params)
    print(response.json())
    data = response.json()['data']
    total = total + sum(data)

print(total)