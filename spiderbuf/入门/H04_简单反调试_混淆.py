import re
import ast # ast = Abstract Syntax Tree（抽象语法树）
import json
import requests


# 将字符串转成 Python 对象（安全，不执行代码）  不执行 而 eval 会执行
data = ast.literal_eval("[1, 2, 3]")
print(data)  # [1, 2, 3]

data = ast.literal_eval("{'name': '张三', 'age': 18}")
print(data)  # {'name': '张三', 'age': 18}


# 这里混淆值得是数据用JS返回 用16进制以及unicode编码部分数据
# 使用 \1 \2 引用分组
re.sub(r'(\d+)-(\d+)', r'\2-\1', '123-456')
# 输出: '456-123'（交换位置）

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1",
    "referer": "https://spiderbuf.cn/web-scraping-practice/javascript-confuse-encrypt-reverse",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775205618$o13$g1$t1775206199$j36$l0$h0"
}
url = "https://spiderbuf.cn/static/js/h04/udSL29.js"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
pattern = re.compile(r"var data=(.*?);var dataContent")
m = re.search(pattern, response.text)

# def decode_unicode(text):
#     # 解码 \uXXXX 格式
#     text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)
#     # 解码 0xX | 0xXX | 0xXXX 格式
#     text = re.sub(r'0x([0-9a-fA-F]{1,2})', lambda m: str(int(m.group(1), 16)), text) # 16进制到10进制
#     text = re.sub(r'0x([0-9a-fA-F]{3})', lambda m: str(int(m.group(1), 16)), text)  # 16进制到10进制
#     return text
# if m:
#     data = m.group(1)
#     decoded_data = decode_unicode(data)
#     print(data)
#     print(decoded_data)

if m:
    data = eval(m.group(1))
    print(data)
    for item in data:
        print(item)
    print("*"*100)
    data2 = ast.literal_eval(m.group(1))
    print(data2)


code = "x = 1 + 2 * 3"
tree = ast.parse(code)
print(ast.dump(tree, indent=2)) # 输出代码的语法树结构
