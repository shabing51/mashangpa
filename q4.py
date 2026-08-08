# import time
# import hashlib
# from curl_cffi import requests

# # 使用标准的md5进行查询参数的编码(加密)
# # window.sign = window.md5("tuling" + timestamp + pageNumber)

# url = "https://www.mashangpa.com/api/problem-detail/4/data/"
# def fetch_params_by_page_num(num):
#     _ts = str(int(time.time()*1000))
#     s = f"tuling{_ts}{num}"
#     sign = hashlib.md5(s.encode("utf-8")).hexdigest()
#     params = {"page": num,
#               "sign": sign,
#               "_ts": _ts,
#     }
#     return params


# def fectch_data_by_page_num(num, session):

#     params = fetch_params_by_page_num(num)
#     resp = session.get(url, params=params)

#     return resp.json().get("current_array")

# def main():
#     print(f"".center(62, '='))
#     total = 0
#     cookies = { ##需要更换 sessionid
#         'sessionid': '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs',
#     }
#     headers = {
#         'pragma': 'no-cache',
#         'referer': 'https://www.mashangpa.com/problem-detail/4/',
#         'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                     'AppleWebKit/537.36 (KHTML, like Gecko) '
#                     'Chrome/151.0.0.0 Safari/537.36'),
#     }
#     session = requests.Session(headers=headers, cookies=cookies)
#     for num in range(1, 21):
#         current_array = fectch_data_by_page_num(num, session)
#         print(f"第{num:2d}页数据: {current_array}")
#         total += sum(current_array)
#         # time.sleep(0.5)

#     print(f"20页数据的和: {total} ".center(56, '='))

# if __name__ == "__main__":
#     main()

#######################################
#############异步 协程#################
######################################
import time
import random
import hashlib
import asyncio
import aiohttp

class AsyncFetcher:
    """爬取问题4的20页数据"""
    def __init__(self,start_url, headers, cookies):
        self.start_url = start_url
        self.headers = headers
        self.cookies = cookies
        self.total = 0

    async def async_fetch_by_page_num(self, num, session):
        await asyncio.sleep(random.choice([0.1, 0.2, 0.3, 0.4]))
        _ts = str(int(time.time()*1000))
        s = f"tuling{_ts}{num}"
        sign = hashlib.md5(s.encode("utf-8")).hexdigest()
        params = {
            "page": num,
            "sign": sign,
            "_ts": _ts,
        }
        resp = await session.get(self.start_url, params=params)
        res = (await resp.json()).get("current_array")
        print(f"第{num:2d}页数据: {res}")
        await asyncio.sleep(random.choice([0.1, 0.2, 0.3, 0.4]))
        return res

    async def main(self):
        async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
            tasks = []
            for page_num in range(1,21):
                task = self.async_fetch_by_page_num(page_num, session)
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            for res in result:
                self.total += sum(res)
    # def __del__(self):

if __name__ == "__main__":
    start_url = ("https://www.mashangpa.com"
                "/api/problem-detail/4/data/")
    cookies = { ##需要更换 sessionid
        'sessionid': '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs',
    }
    headers = {
        'pragma': 'no-cache',
        'referer': 'https://www.mashangpa.com/problem-detail/4/',
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/151.0.0.0 Safari/537.36'),
    }

    af = AsyncFetcher(start_url, headers, cookies)
    asyncio.run(af.main())
    print(f"20页数据的和: {af.total} ".center(56, '='))
