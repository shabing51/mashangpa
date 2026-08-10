import requests
import pandas as pd
from lxml import etree, html

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/2?order=rating",
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
    "_ga": "GA1.1.261017283.1775044945",
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775051069$j54$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/lxml-xpath-advanced"
response = requests.get(url, headers=headers, cookies=cookies)


tree = html.fromstring(response.text)
table = tree.xpath("//table[@class='table']")[0]  # 使用xpath返回一定是列表

header = [th.text_content().strip() for th in table.xpath("./thead/tr/th")]
# print(header)
# 提取数据
data = []  # text_content()：获取元素及其所有子元素的完整文本   # xpath('//text()'): 返回文本列表
# text_content(): 拼接所有文本
for tr in table.xpath(".//tbody/tr"):
    row_data = [td.text_content().strip() for td in tr.xpath("./td")]
    data.append(row_data)
df = pd.DataFrame(data, columns=header)
print(df.to_string(index=False))


