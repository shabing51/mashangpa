import json
import execjs
from loguru import logger
from curl_cffi import requests

with open("./yrx/aqistudy.js", "r", encoding="utf-8") as fr:
    js_code = fr.read()
ctx = execjs.compile(js_code)

headers = {
    "Content-Type": ("application/x-www-form-urlencoded; "
                     "charset=UTF-8"),
    "Origin": "https://www.aqistudy.cn",
    "Referer": ("https://www.aqistudy.cn"
                "/historydata/daydata.php?"
                "city=%E6%98%86%E6%98%8E&"
                "month=202507"),
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/150.0.0.0 Safari/537.36"),
    "X-Requested-With": "XMLHttpRequest",
}

url = "https://www.aqistudy.cn/historydata/api/historyapi.php"
obj = {
    "city": "昆明",
    "month": "202607",
}
data = ctx.call("getReqBody", obj)
logger.info(f"请求数据：{data}")
response = requests.post(url, headers=headers, data=data)

logger.info(f"响应数据密文：{response.text}")
logger.info(f"响应数据明文：{json.loads(ctx.call('dxvERkeEvHbS', response.text))}")