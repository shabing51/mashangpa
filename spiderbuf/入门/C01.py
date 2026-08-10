from curl_cffi import requests
from io import StringIO
import pandas as pd
import numpy as np

session = requests.Session()
session.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"})
# 设置响应cookie
session.get('https://spiderbuf.cn/challenge/scraper-practice-c01')
# 拿数据
resp = session.get('https://spiderbuf.cn/challenge/scraper-practice-c01/mnist')
resp.raise_for_status()
html = resp.content.decode('utf-8')

html_io = StringIO(html)
df = pd.read_html(html_io)[0]

a = df['Pix1'].to_numpy()
b = np.mean(a)
print(a)
print(b, round(b,2))
