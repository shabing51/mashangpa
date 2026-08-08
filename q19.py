from curl_cffi import requests
import json
import execjs
with open('./q19.cjs', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)


headers = {
    "referer": "https://www.mashangpa.com/problem-detail/19/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}
url = "https://www.mashangpa.com/api/problem-detail/19/data/"
total = 0
for page_num in range(1, 21):
    params = {
        "page": str(page_num)
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).json()

    raw_data = ctx.call("myDecrypt", response['r'], response['k'])

    data = json.loads(raw_data)['current_array']
    print(f"第{page_num:02d}页数据: {data}")
    total += sum(data)
print(f"{total=}")