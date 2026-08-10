import re
import hashlib
import base64
import ddddocr
from bs4 import BeautifulSoup
from curl_cffi import requests

def hex_md5(strr:str)->str:
    return hashlib.md5(strr.encode()).hexdigest()
def btoa(strr:str)->str:
    return base64.b64encode(strr.encode()).decode()

ocr = ddddocr.DdddOcr(show_ad=False)

headers = {
    "referer": "https://match.yuanrenxue.cn/match/4",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "qcngxf1p24fbthxucr94o1std0qhdms8"
}
url = "https://match.yuanrenxue.cn/api/question/4"


total = 0 
for page_num in range(1,6):
    params = {
        "page": str(page_num),
        "pageSize": "10",
        "kw": ""
    }
    data = requests.get(url, headers=headers, cookies=cookies, params=params).json()

    key, value, info = data['key'], data['value'], data['info']
    # CSS选择器
    hide_cls = hex_md5(btoa(key + value).replace('=', ''))

    soup = BeautifulSoup(info,"html.parser")

    # 10个td对应10个数字，td里面包含多个img标签
    numbers = [] # 存储10个数字
    for td in soup.find_all("td"):
        ind = 0
        num_left = {}
        for img in td.find_all("img"):
            cls = img.get("class", '')
            # print(cls) # ['img_number', '66af83adc9f91aac59cea46776190dee']
            # 若包含特定class，display:none
            if cls and hide_cls in cls:
                continue
            # 获取left
            style = img.get("style","")
            assert isinstance(style, str)
            left = float(re.search(r"left:([\-\d.]+)px", style).group(1)) # type: ignore

            src = img.get('src', '')
            assert isinstance(src, str)
            # 贪婪正后顾
            match = re.search(r'(?<=base64,).*', src, re.DOTALL)
            if match:
                b64img = match.group()
                num = ocr.classification(base64.b64decode(b64img))
                num_left[ind] = (num, left)
                ind += 1

        temp_dic = {}
        for k,(num,left) in num_left.items():
            pos = k + round(left / 8.5)
            temp_dic[pos] = num

        num_str = ''.join(temp_dic[k] for k in sorted(temp_dic))

        numbers.append(int(num_str))
    print(f"第{page_num}页数据: {numbers}")

    total += sum(numbers)
    
print(f"total is {total}")
    