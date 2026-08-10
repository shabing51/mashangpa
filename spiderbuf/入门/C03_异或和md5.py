import json
import time
import random
import hashlib
import requests
from math import floor

big_data = []
url = "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c03"
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
           "referer": "https://spiderbuf.cn/web-scraping-practices/5?order=rating",
           "cookie": "_ga=GA1.1.556439622.1775108645; _ga_7B42BKG1QE=GS2.1.s1775131837$o5$g1$t1775131874$j23$l0$h0"
}

for page_num in range(1, 6):
    timestamp = int(time.time())
    random_num = floor( random.random() * 8000 + 2000 )
    xor_res = timestamp ^ page_num
    s_bytes = (str(xor_res) + str(timestamp)).encode('utf-8')
    payload = {
        "xorResult": xor_res,   # 时间戳（秒级别）与 页码 异或
        "random":random_num,    # random_num写死没毛病 # floor(8000 * random.random() + 2000) # 应该可以写死只要在2000 ~ 10000 以内的整数
        "timestamp": timestamp, # 时间戳 不用乘以1000转换为毫秒级别，就是秒级别的 需要取整
        "hash": hashlib.md5(s_bytes).hexdigest()   # 标准MD5(xorResult+timestamp)
    }

    response = requests.post(url=url, headers=headers, json=payload)
    # response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    json_data = response.json()
    big_data.extend(json_data)
    print(json_data)

print(len(big_data)) # 150
print(big_data)

total = 0
for item in big_data:
    total += item.get("sepal_width")
print(round(total, 3))
print(round(total, 2))

















#  场景	    位置	          作用	                   示例
# 请求头	客户端 → 服务器	告诉服务器我发送的数据格式	Content-Type: application/json
# 响应头	服务器 → 客户端	告诉客户端服务器返回的数据格式	Content-Type: text/html
"""
import requests

# 发送 JSON 数据
headers = {
    "Content-Type": "application/json"  # 告诉服务器：我发的是 JSON
}
data = {"name": "张三", "age": 18}
requests.post(url, headers=headers, json=data)

# 发送表单数据
headers = {
    "Content-Type": "application/x-www-form-urlencoded"  # 告诉服务器：我发的是表单
}
data = "name=张三&age=18"
requests.post(url, headers=headers, data=data)

# 发送文件
headers = {
    "Content-Type": "multipart/form-data"  # 告诉服务器：我发的是文件
}
files = {"file": open("test.jpg", "rb")}
requests.post(url, headers=headers, files=files)
"""

"""
import requests

response = requests.get(url)
content_type = response.headers.get("Content-Type")

print(content_type)
# 可能的输出：
# "text/html"          → HTML 网页
# "application/json"   → JSON 数据
# "image/jpeg"         → JPEG 图片
# "application/pdf"    → PDF 文件
# "text/plain"         → 纯文本
"""