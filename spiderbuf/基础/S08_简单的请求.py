import requests
import pandas as pd
from lxml import etree,html
from bs4 import BeautifulSoup


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://spiderbuf.cn",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-via-http-post",
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
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775045101$j57$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/scraper-via-http-post"
data = {
    "level": "8"
}
response = requests.post(url, headers=headers, cookies=cookies, data=data)

# 方式1
# 提取数据 提取表格
from io import StringIO
html_io = StringIO(response.text)
table = pd.read_html(html_io)[0]
print("*" * 50 + "方式1_read_html" + "*" * 50)

print(table.to_string(index=False))


# 方式2
print("*" * 50 + "方式2_bs4" + "*" * 50)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', class_='table')   # attrs = {"class" : "table"}

# 手动提取表格数据
data = []
headers = [th.text.strip() for th in table.find('thead').find_all('th')]

for row in table.find('tbody').find_all('tr'):
    row_data = [td.text.strip() for td in row.find_all('td')]
    data.append(row_data)
# 转换为 DataFrame
df = pd.DataFrame(data, columns=headers)
print(df.to_string(index=False))



print("*" * 50 + "方式3_lxml" + "*" * 50)
# 使用 lxml 解析
tree = html.fromstring(response.content)
table = tree.xpath('//table[@class="table"]')[0]
# 提取表头
headers = [th.text_content().strip() for th in table.xpath('.//thead/tr/th')]
# 提取数据行
data = []
rows = table.xpath('.//tbody/tr')
for row in rows:
    row_data = [td.text_content().strip() for td in row.xpath('.//td')]
    data.append(row_data)
# 创建 DataFrame
df = pd.DataFrame(data, columns=headers)
print(df.to_string(index=False))