import requests
import pandas as pd
from lxml import etree


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
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775053666$j60$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/requests-lxml-for-scraping-beginner"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
tree = etree.HTML(response.text)
table = tree.xpath("//table[@class='table']")[0]   # 列表的第一个
columns = [th.text.strip() for th in table.xpath("./thead/tr/th")]
# print(columns)
data_all = []
for tr in table.xpath(".//tbody/tr"):   # 缺少单元格数据处理
    data_row = [td.text.strip() if td.text else "NAN" for td in tr.xpath("./td")]
    data_all.append(data_row)
df = pd.DataFrame(data_all, columns=columns)
print(df.to_string(index=False))