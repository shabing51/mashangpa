import re
import time
import random
import string
import hashlib
import requests
import pandas as pd



def generate_key_and_timestamp():
    # 获取当前时间戳（秒）
    timestamp = int(time.time())

    # 随机字符串字符集
    characters = string.ascii_letters + string.digits  # 62个字符

    # 生成32位随机字符串
    key = ''.join(random.choice(characters) for _ in range(32))

    return timestamp, key


headers = {
    "referer": "https://spiderbuf.cn/web-scraping-practices/8?order=rating",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
,}

url = "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c07"
response = requests.get(url, headers=headers)

token = re.findall(r'<input type=\"hidden\" name=\"token\" id=\"token\" value=\"(.*?)\">', response.text)[0]

timestamp, key = generate_key_and_timestamp()
payload ={
    "token": token,
    "key": key,
    "timestamp": timestamp,
}
# print(payload)
headers["referer"] = url
s = f"{timestamp}{token}{key}"
_md5 = hashlib.md5(s.encode()).hexdigest()

cookies = {'_asd2sdf99': _md5}
resp = requests.post(url, headers=headers, cookies=cookies, json=payload)
if resp.status_code == 200:
    data_json = resp.json()
    df = pd.DataFrame(data_json)
    df["CPC"] = (df["cpc_usd"] ^ df["monthly_search_volume"]) / 100
    print(f"CPC均值: {df['CPC'].mean()}")
else:
    print(resp.text)

