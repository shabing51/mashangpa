import requests
import execjs
import subprocess
import re
import ast

cookies = {
    "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs",
}

url = "https://www.mashangpa.com/api/problem-detail/13/data/"
total = 0
for pageNumber in range(1,21):
    result = subprocess.check_output(['node', './q13.js', str(pageNumber)], text=True).strip()
    data_str= re.sub(r'(\w+):', r'"\1":', result)  # 键名加引号
    # json_str = re.sub(r"'", '"', data_str)         # 单引号变双引号
    headers_str = re.sub(r': (\w+),', r': "\1",', data_str)

    headers = ast.literal_eval(headers_str)
    data = f"""{{"page":"{pageNumber}"}}"""

    resp = requests.post(url, headers=headers, cookies=cookies, data=data)
    current_array = resp.json().get("current_array")

    print(f"第{pageNumber:02d}页数据: {current_array}")
    total += sum(current_array)
print(f"{total=}")