import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

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
    "_ga": "GA1.1.261017283.1775044945",
    "_ga_7B42BKG1QE": "GS2.1.s1775094572$o2$g1$t1775098930$j44$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/scraping-random-pagination"
response = requests.get(url, headers=headers, cookies=cookies)

base_url = 'https://spiderbuf.cn'

soup = BeautifulSoup(response.text, "lxml")
# print(soup.prettify())

a_s = soup.select("nav > ul > li > a")  # 类似列表的返回值
# print("a_s", a_s)
"""
a_s [<a class="item" href="/web-scraping-practice/block-ip-proxy/2fe6286a4e5f">1</a>, <a class="item" href="/web-scraping-practice/block-ip-proxy/5f685274073b">2</a>, <a class="item" href="/web-scraping-practice/block-ip-proxy/279fcd874c72">3</a>, <a class="item" href="/web-scraping-practice/block-ip-proxy/8a3d4d640516">4</a>, <a class="item" href="/web-scraping-practice/block-ip-proxy/fbd076c39d28">5</a>]
"""
urls = []
for a in a_s:
    path = a.get('href')
    url = base_url + path
    urls.append(url)

def get_by_url(url):
    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"})
    html_io = StringIO(response.text)
    df = pd.read_html(html_io)[0]
    return df


all_dfs = [get_by_url(url) for url in urls]
all_dfs = pd.concat(all_dfs)  # 将列表中的所有DataFrame垂直拼接（合并）成一个大的DataFrame
all_dfs = all_dfs.reset_index(drop=True)  # drop=True 表示丢弃原来的索引，从0开始重新编号
all_dfs = all_dfs.to_dict(orient='records')  # orient='records' 表示每行数据转换为一个字典，所有字典组成一个列表
df = pd.DataFrame(all_dfs, columns=['排名',"企业估值(亿元)","企业信息","CEO","行业"], index=range(1,len(all_dfs)+1))
print(df)