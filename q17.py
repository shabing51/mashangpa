import re
import ast
import time
import hashlib
from logging import exception

import requests

"""
const FONT_DECRYPT_MAP = {
    'ꙮ': '0',
    'ઊ': '1',
    'સ': '2',
    'ત': '3',
    'ধ': '4',
    'ન': '5',
    'પ': '6',
    'ફ': '7',
    'બ': '8',
    'ભ': '9'
};
"""

def trans(s, map=None):
    digits = []
    for x in s:
        digits.append(map.get(x, x))
    try:
        return int(''.join(digits))
    except Exception as e:
        print("Error", e)
        return "".join(digits)




if __name__ == '__main__':
    # 获取 FONT_DECRYPT_MAP
    response = requests.get('https://www.mashangpa.com/static/js/pagination17.js')
    font_map_str = re.findall("const FONT_DECRYPT_MAP=(?P<font_map>.*?);", response.text)[0]
    font_map = ast.literal_eval(font_map_str) #  JSON 规范要求键名和字符串值必须使用双引号
    # 获取数据
    base_url = "https://www.mashangpa.com/api/problem-detail/17/data/"
    cookies = {"sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs"}

    total = 0
    for pageNumber in range(1, 21):
        params = {
            "page": pageNumber
        }
        response = requests.get(base_url, params=params, cookies=cookies)
        current_array = response.json().get('current_array')
        # 根据映射还原数据
        dataList = [trans(numberStr, map=font_map) for numberStr in current_array]
        print(f"第{pageNumber:2d}页的数据: {dataList}")
        total += sum(dataList)
    print(total)