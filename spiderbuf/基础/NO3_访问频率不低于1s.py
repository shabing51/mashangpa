import time
import random
import requests
import pandas as pd
from io import StringIO

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-bypass-request-limit/2",
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
    "_ga_7B42BKG1QE": "GS2.1.s1775125554$o4$g1$t1775127644$j1$l0$h0"
}
all_df = []
for page_num in range(1, 21):
    url = "https://spiderbuf.cn/web-scraping-practice/scraper-bypass-request-limit/{}".format(page_num)
    response = requests.get(url, headers=headers, cookies=cookies)
    html_io = StringIO(response.text)
    table_df = pd.read_html(html_io)[0]
    all_df.append(table_df)
    t = random.random() + 0.5
    print(page_num,  t)
    time.sleep(t) # 睡一会儿


big_df = pd.concat(all_df, ignore_index=True)
print(big_df.to_string(index=False))