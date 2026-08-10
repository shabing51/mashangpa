import requests
import pandas as pd
from io import StringIO


session = requests.Session()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://spiderbuf.cn",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-login-username-password",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}

# 登录不用带cookie, 登录后会有admin cookie
session.headers.clear()
session.headers.update(headers)
url = "https://spiderbuf.cn/web-scraping-practice/scraper-login-username-password/login"
data = {
    "username": "admin",
    "password": "123456"
}
response = session.post(url, headers=headers, data=data)

url = "https://spiderbuf.cn/web-scraping-practice/scraper-login-username-password/list"

response = session.get(url)
# print(session.cookies)  # <RequestsCookieJar[<Cookie admin=69b9f4da7f261e0fb94e95b250b3522f for .spiderbuf.cn/>]>
html_io = StringIO(response.text)
df_table = pd.read_html(html_io)[0]
print(df_table.to_string(index=False))

