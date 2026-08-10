import crawles
import base64
from bs4 import BeautifulSoup


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/4?order=rating",
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
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775116100$o2$g1$t1775118577$j44$l0$h0"
}
# base64: A-Za-z0-9+/
url = "https://spiderbuf.cn/web-scraping-practice/scraping-images-base64"
res = crawles.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(res.text, "lxml")
img = soup.find_all("img")[0]
src = img.get("src")
data = src.split(",")[1]

img_bytes = base64.b64decode(data)
with open (r"./N02_bsae64.png", "wb") as f:
    f.write(img_bytes)
print("ok")