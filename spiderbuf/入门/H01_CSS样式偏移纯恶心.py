import requests
import pandas as pd
from lxml import etree

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/6?order=rating",
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
    "_ga_7B42BKG1QE": "GS2.1.s1775214779$o15$g1$t1775219430$j60$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/scraping-css-confuse-offset"
response = requests.get(url, headers=headers, cookies=cookies)

root= etree.HTML(response.text)
divs = root.xpath('//div[@class="col-xs-6 col-lg-4"]')

data = []
for div in divs:
    list_ = div.xpath('.//h2//i/text()')
    list_[0], list_[1] = list_[1], list_[0]
    title = ''.join(list_)
    rank = ''.join(div.xpath('./p[1]/text()')).replace("排名：", '')
    value_ = div.xpath('./p[2]/i/text()')
    value_[0], value_[1] = value_[1], value_[0]
    valuation = ''.join(value_)
    ceo = div.xpath('./p[3]/text()')[0]
    service = div.xpath('./p[4]/text()')[0]
    data.append([title, rank, valuation, service, ceo])

df = pd.DataFrame(data, columns=['title', 'rank', 'value_', 'service', 'ceo'])
print(df.to_string(index=False))