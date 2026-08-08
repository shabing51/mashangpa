import requests
import json
import subprocess


headers = {
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.mashangpa.com",
    "referer": "https://www.mashangpa.com/problem-detail/16/",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"),
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}
url = "https://www.mashangpa.com/api/problem-detail/16/data/"

total = 0
for page_num in range(1, 21):
    ppp = subprocess.run(["node", "./q16.cjs", str(page_num)], capture_output=True, text=True).stdout
    json_data = json.loads(ppp)
    data = {
        "page": page_num,
        "t": json_data["t"],
        "h5": json_data["h5"],
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    current_array = response.json()['current_array']
    print(f"第{page_num:02d}页数据: {current_array}")
    total += sum(current_array)

print(f"{total=}")
