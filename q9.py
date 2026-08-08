import requests
import re,os
import ast
import subprocess
import time
import random
import hashlib,hmac, base64
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent

def fx(page):
    f = str(int(time.time()*1000))
    m = hmac.new("xxxooo".encode(), 
                         f"9527{f}".encode(), 
                         hashlib.sha1).hexdigest()
    tt = base64.b64encode(f.encode()).decode()
    return {
        "page": str(pageNumber),
        "m": m,
        "tt":tt
    }

headers = {
    "content-type": "application/json",
    "origin": "https://www.mashangpa.com",
    "referer": "https://www.mashangpa.com/problem-detail/9/",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/147.0.0.0 Safari/537.36"),
}
cookies = {  ##需要更换 sessionid
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}

url = "https://www.mashangpa.com/api/problem-detail/9/data/"

total = 0
for pageNumber in range(1,21):
    # # os.popen subprocess.run execjs
    # result = subprocess.check_output(['node', BASE_DIR / 'q9.cjs', f"{pageNumber}"], text=True)
    # data = re.sub(r'(\w+):', r'"\1":', result)  # 键名加引号
    # # json_str = re.sub(r"'", '"', json_str)  # 变双引号
    # data = ast.literal_eval(data) 

    data = fx(pageNumber)

    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    current_array = response.json().get("current_array")
    print(f"第{pageNumber:02d}页数据: {current_array}")
    total += sum(current_array)

print(f"20页数据的和: {total} ".center(56, '='))


