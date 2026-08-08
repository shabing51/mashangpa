import aiohttp
import asyncio
import execjs
import json

with open('./q18.cjs', 'r', encoding='utf8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

url = "https://www.mashangpa.com/api/problem-detail/18/data/"
cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}
headers = {
    "client-version": "1.0.0",
    "referer": "https://www.mashangpa.com/problem-detail/18/",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"),
    "x-requested-with": "XMLHttpRequest"
}

sem = asyncio.Semaphore(2)

async def fetch_data(page:int, session:aiohttp.ClientSession) -> list[int]:
    async with sem:
        req_headers = {
            **headers,
            **json.loads(ctx.call('result'))
        }
        # print(json.loads(ctx.call('result')))
        resp = await session.get(url, params={'page': page}, headers=req_headers)
        raw_data = await resp.json()
     
        data_ = raw_data['current_array']
        print(f"第{page:02d}页数据: {data_}")
        return data_

async def main():
    total_ = 0

    connector = aiohttp.TCPConnector(
        limit=10,
        ssl=False
    )
    async with aiohttp.ClientSession(cookies=cookies, connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
        tasks = [asyncio.create_task(fetch_data(page, session)) for page in range(1, 21)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # for res in results:
        #     if isinstance(res, Exception):
        #         print(res)
        #         continue
        #     total_ += sum(res)
        total_ = sum( sum(res) for res in results if isinstance(res, list) )
        return total_



if __name__ == "__main__":
    total = asyncio.run(main())
    print(f"{total=}")