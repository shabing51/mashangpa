import requests
import pprint
from lxml import html

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/3?order=rating",
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
    "_ga_7B42BKG1QE": "GS2.1.s1775108645$o1$g1$t1775111617$j60$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/scraping-form-rpa"
response = requests.get(url, headers=headers, cookies=cookies)

pprint.pprint(response.text)

tree = html.fromstring(response.text)
form = tree.xpath("/html/body/main/div[2]/div/form")[0]  # 又出错了 xpath 一定是列表呀
for div in form.xpath('.//div'):
    label = div.xpath(".//label/text()")
    input = div.xpath(".//input/@value")
    if label:
        print(label, input)