import requests
import pandas as pd
from io import StringIO


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraping-iframe",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
cookies = {
    "_ga": "GA1.1.261017283.1775044945",
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775047502$j35$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/inner"
response = requests.get(url, headers=headers, cookies=cookies)

# print(response.text)

html_io = StringIO(response.text)
data_table = pd.read_html(html_io)[0]
print(type(data_table))
print(data_table.to_string(index=False))