import requests
import subprocess
import time


headers = {
    "referer": "https://www.mashangpa.com/problem-detail/12/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}
base_url = "https://www.mashangpa.com"
total = 0
for page in range(1, 21):
    url = base_url + subprocess.run(['node', './q12.cjs', str(page)], capture_output=True, text=True).stdout.strip()
    print(url)

    response = requests.get(url, headers=headers, cookies=cookies)
    current_array = response.json()['current_array']
    print(f"第{page:02d}页数据: {current_array}")
    time.sleep(1)
    total += sum(current_array)
print(f"{total=}")
