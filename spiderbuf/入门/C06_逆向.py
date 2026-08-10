import time
import json
import hashlib
import requests
from lxml import etree

session = requests.Session()
session.headers.clear()
session.cookies.clear()
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://spiderbuf.cn",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c06",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
# cookies = {
#     "_ga": "GA1.1.556439622.1775108645",
#     # "_asd2sdf99": "gvGAJJbfZxDhI17Eu59KPhAkT1nzJ6zM",
#     "_ga_7B42BKG1QE": "GS2.1.s1775214779$o15$g1$t1775224820$j49$l0$h0"
# }
session.headers.update(headers)
# session.cookies.update(cookies)
url = "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c06"


response_get = session.get(url)

root = etree.HTML(response_get.text)
print(list(map(float, root.xpath("//div[@class='detail']/p[1]/span[2]/text()"))))
partial_rating_sum = sum(map(float, root.xpath("//div[@class='detail']/p[1]/span[2]/text()")))
print(partial_rating_sum)

print(session.cookies)


def generate_token():
    # random_num = random.randint(2000, 10000)
    random_num = 4648
    timestamp = int(time.time())
    sign_str = f"{random_num}spiderbuf{timestamp}"
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    return random_num, timestamp, sign
# f = "6168"+"spiderbuf"+"17752224822"
# print(hashlib.md5((f).encode('utf-8')).hexdigest())

random_num, timestamp, sign = generate_token()
print(random_num, timestamp, sign)

data = {
    "random": 4648,
    "timestamp": timestamp,
    "signture": sign
}
data = json.dumps(data, separators=(',', ':'))
response = session.post(url, data=data).json()
sum_ = 0.0
for item in response:
    d = float(item.get("rating"))
    sum_ += d
    print(d)

print(sum_)
print(f"total: {(sum_+partial_rating_sum):.3f}")