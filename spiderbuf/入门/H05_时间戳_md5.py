import time
import base64
import hashlib
from curl_cffi import requests

def get_param():
    timestamp =int(time.time() * 1)
    _md5 = hashlib.md5(str(timestamp).encode('utf-8')).hexdigest()
    s_tmp = f"{timestamp},{_md5}"
    s = base64.b64encode(s_tmp.encode('utf-8')).decode('utf-8')
    return s

base_url = "https://spiderbuf.cn/web-scraping-practice/javascript-reverse-timestamp/api/"

url = f"{base_url}{get_param()}"

# 发请求， 拿数据
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(resp.json())