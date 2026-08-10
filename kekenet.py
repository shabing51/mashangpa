from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def un(e, a='51E881E6F2A6Y9K8', t="9F0885C2D686C418"):
    cipher = AES.new(
        a.encode(),
        mode=AES.MODE_CBC,
        iv=t.encode(),
    )
    padded_data = pad(e.encode(), AES.block_size)
    o = cipher.encrypt(padded_data).hex().upper()
    return o


from curl_cffi import requests
import json
import time

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "text/plain",
    "Origin": "https://www.kekenet.com",
    "Pragma": "no-cache",
    "Referer": "https://www.kekenet.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
}
url = "https://mob2015.kekenet.com/keke/mobile/index.php"
username = 'shabing'
password = '123456'
data = {
    "Method": "web_user_login",
    "Params": {
        "username": un(username),
        "password": un(password),
        "type": 0
    },
    "Token": "",
    "Terminal": 13,
    "Version": "4.0",
    "UID": "",
    "AppFlag": 18,
    "Sign": "",
    "ApTime": int(time.time()*1000),
    "ApVersionCode": 100
}

data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)

print(response.json())

