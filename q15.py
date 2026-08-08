import requests
import os


headers = {
    "referer": "https://www.mashangpa.com/problem-detail/15/",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/151.0.0.0 Safari/537.36")
}

url = "https://www.mashangpa.com/api/problem-detail/15/data/"
total = 0
for i in range(1, 21):
    cookies = {
        "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
        "v": os.popen("node ./q15.cjs").read().strip()
    }
    params = {
        "page": str(i),
    }
    response = requests.get(url, headers=headers, 
                            cookies=cookies, params=params)

    data = response.json().get("current_array")
    total += sum(data)
    print(f'第{i:02d}页数据: {data}')

print(f"{total=}")