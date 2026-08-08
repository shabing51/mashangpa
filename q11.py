import aiohttp
import asyncio
import json
import execjs
import random
import time
from curl_cffi import requests

headers = {
    "referer": "https://www.mashangpa.com/problem-detail/11/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}

url = "https://www.mashangpa.com/api/problem-detail/11/data/"
# 编译JS
with open("./q11.js","r",encoding="utf-8") as fr:
    js_code = fr.read()
ctx = execjs.compile(js_code)
# js_lock = asyncio.Lock()
sem = asyncio.Semaphore(6)

async def get_data(page_num, session):
    async with sem:
        ret = await asyncio.to_thread(
            ctx.call,
            "loadPage",
            str(page_num)
        )
        params = json.loads(ret)

        async with session.get(url, params=params) as response:
            data = await response.json()
            await asyncio.sleep(random.random()+0.5)
            print(f"第{page_num:02d}页数据为: {data["current_array"]}")
            return data["current_array"]

async def main():
    total = 0
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        tasks = [asyncio.create_task(get_data(page_num=page_num, session=session) ) for page_num in range(1, 21)]
        results = await asyncio.gather(*tasks)
        total = sum(
            sum(x)
            for x in results
        )
        return total
def get_all_data():
    sum_ = 0
    for page in range(1, 21):
        resp = requests.get(url, params=json.loads(ctx.call("loadPage", str(page))), headers=headers, cookies=cookies)
        resp.raise_for_status()
        current_array = resp.json()["current_array"]
        print(f"第{page:02d}页数据为: {current_array}")
        sum_ += sum(current_array)
    print(f"20页数据的和: {sum_} ".center(56, '='))
    return sum_
if __name__ == "__main__":
    print(f"".center(62, '='))
    start = time.time()
    result = asyncio.run(main())
    # print("总和:", result)
    end = time.time()
    print(end - start)


    start = time.time()
    res = get_all_data()
    # print("总和:", res)
    end = time.time()
    print(end - start)
"""
# page_num = 2
# with open('./shabing.js', 'r', encoding='utf-8') as f:
#     js_code = f.read()
# ctx = execjs.compile(js_code)
# params = json.loads(ctx.call("loadPage", str(page_num)))
# print(params)
# response = requests.get(url, headers=headers, cookies=cookies, params=params)
# current_array = response.json().get('current_array', [])
# print(current_array)


page_num = 2
with open('./shabing.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
ts = str(int(time.time()))
m = ctx.call('encrypt', page_num, ts)
print(m,type(m))
params = {
    "page": str(page_num),
    "m": m,
    "_ts": str(int(time.time()))
}
print(params)
response = requests.get(url, headers=headers, cookies=cookies, params=params)
current_array = response.json().get('current_array', [])
print(current_array)
"""