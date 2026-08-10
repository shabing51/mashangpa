import re
import json
import base64
import requests
import pandas as pd

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c04",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775286059$o20$g1$t1775286408$j60$l0$h0"
}
url = "https://spiderbuf.cn/static/js/c04/lhY3nm7.min.js"
response = requests.get(url, headers=headers, cookies=cookies)

data_b64 = re.findall("from\',\'(.*?)\',\'webdriver", response.text)[0]
# 好像多了两个字符，额,不管，切掉就行
# print(data_b64)
data = base64.b64decode(data_b64).decode().replace("d", '')
# for item in data:
#     int(item.get("reads", 0)) + int(item.get("comments", 0))
json_data = json.loads(data)
df = pd.DataFrame(json_data, columns=["title", "content", "reads", "likes", "shares", "comments"])
df["reads_plus_comments"] = df["reads"] + df["comments"]
mean_v, std_v, sum_ = df["reads_plus_comments"].agg(['mean', 'std', 'sum'])

print(df.to_string(index=False))
print(f"阅读量与评论量之和的均值: {mean_v} 标准差: {std_v} 总和: {sum_}")






