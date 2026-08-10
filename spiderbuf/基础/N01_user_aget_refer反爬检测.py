from curl_cffi import requests
# from lxml import html
from bs4 import BeautifulSoup
import re
import pprint
"""
📖 BeautifulSoup 的 string 参数支持的匹配方式
匹配方式	        示例	                                      说明
精确字符串	    string="排名："	                          必须完全相等
正则表达式	    string=re.compile('排名')	              包含即可（模糊匹配）
列表	            string=["排名：", "排名"]	                  匹配列表中任一
函数/Lambda   	string=lambda x: x and '排名' in x	    自定义逻辑
True/False	    string=True	                          匹配有文本内容的标签
"""
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "referer": "https://spiderbuf.cn/web-scraping-practices/4?order=rating",
}

url = "https://spiderbuf.cn/web-scraping-practice/user-agent-referrer"

res = requests.get(url, headers=headers,)
# tree = html.fromstring(res.text)
soup = BeautifulSoup(res.text, "lxml")
print(soup)
divs = soup.select("div.col-xs-6.col-lg-4")
all_data = []
for div in divs:
    title = div.find('h2').text
    rank = div.find('p', string=lambda x: x and "排名：" in x).text.split("：")[-1]
    valuation = div.find('p', string=lambda x: x and "企业估值" in x).text.split("：")[-1] + "亿元"
    CEO = div.find("p", string=re.compile("CEO：")).text.split("：")[-1]
    service = div.find("p", string=lambda x: x and "行业：" in x).text.split("：")[-1]
    all_data.append({"title": f"{title}", "rank": f"{rank:2s}", "valuation": valuation, "service": f"{service}"})


for data in all_data:
    pprint.pprint(data)