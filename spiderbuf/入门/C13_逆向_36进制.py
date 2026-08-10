"""
X-Sign:第一次请求没有，后面的请求才会有，每次都从前一次响应里拿
X-Timestamp: Date.now()
X-token: Math.random.toString(36).substring(2,15) + Math.random.toString(36).substring(2,15)
第一次请求仅有 X-Timestamp与X-token后续X-token也是从前一次响应拿
"""
import time
import json
import ctypes

import random
import base64
import requests
import numpy as np
import pandas as pd


# 矢量化
def js_xor_vectorized(a, b):
    """
    向量化的 js_xor，支持 Series
    """
    # 转为整数（向零取整） 只保留整数部分
    a_int = a.astype(np.int64)
    b_int = b.astype(np.int64)

    # 限制在32位无符号范围 注: # 任何数 & 全1 = 该数本身（在32位范围内）
    a32 = a_int & 0xFFFFFFFF # 32位 1
    b32 = b_int & 0xFFFFFFFF # & 0xFFFFFFFF 将数字限制在32位内（截断高位）对于负数，这会产生它的32位补码表示

    # 异或运算
    result = a32 ^ b32

    # 转为有符号（如果需要）
    result = result.where(result <= 0x7FFFFFFF, result - 0x100000000)

    return result
# Test
# df["CPC"] = js_xor_vectorized(df["cpc_usd"], df["monthly_search_volume"]) / 100
# print(df)
def js_xor_series(series_a, series_b):
    """处理两个 Series"""
    return pd.Series([
        js_xor(a, b) for a, b in zip(series_a, series_b)
    ], index=series_a.index)
# df["CPC"] = js_xor_series(df["cpc_usd"], df["monthly_search_volume"]) / 100
# 标量的
def js_xor(a, b):
    """使用 ctypes 模拟JS的32位整数转换"""
    # 转为32位有符号整数
    a32 = ctypes.c_int32(int(a)).value
    b32 = ctypes.c_int32(int(b)).value
    return a32 ^ b32

def js_bitwise_xor(a, b):
    """
    模拟 JavaScript 的 ^ 运算符
    JS会先将操作数转为32位有符号整数
    """

    def to_int32(value):
        # 1. 先转为整数（向零取整）
        if isinstance(value, float):
            # JS的ToInt32: 先取整，再转32位
            value = int(value) if value >= 0 else -int(-value)

        # 2. 转为32位有符号整数
        value = value & 0xFFFFFFFF # 与32个1进行按位与运算,   截断  为最多32位
        if value > 0x7FFFFFFF:    # print(0xFFFFFFFF//2 == 0x7FFFFFFF == 0xFFFFFFFF>>1) # True
            value = value - 0x100000000  # 16**8 = 2^32   有符号和无符号是模 2^32 的同一个剩余类
        return value

    a_int32 = to_int32(a)
    b_int32 = to_int32(b)

    # 按位异或
    result = a_int32 ^ b_int32

    # 保持32位有符号
    if result < 0:
        result = result & 0xFFFFFFFF

    return result
# Test
print("js_bitwise_xor(52.5, 135000)",js_bitwise_xor(52.5, 135000))  # 135020
print("js_bitwise_xor(52, 135000)",js_bitwise_xor(52, 135000))  # 135020

# 将标量函数向量化   ******* +++ ++++====+++++ +++++******
js_xor_vec = np.vectorize(js_xor)
# df["CPC"] = js_xor_vec(df["cpc_usd"], df["monthly_search_volume"]) / 100
# print(df)

def int_to_base36(num: int) -> str:
    """
    将整数转换为36进制字符串
    """
    if num == 0:
        return "0"

    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""

    # 处理负数
    is_negative = num < 0  # flag
    num = abs(num)

    # 不断取余数
    while num > 0:
        remainder = num % 36
        result = chars[remainder] + result # 除 k 取余法 结果要逆 所以不是  X result = result + chars[remainder] X
        num //= 36

    return "-" + result if is_negative else result
def float_to_base36(num: float, precision: int = 11) -> str:
    """
    将小数转换为36进制字符串
    """
    # 分离整数和小数部分
    int_part = int(num)
    frac_part = num - int_part

    # 转换整数部分
    int_str = int_to_base36(int_part) if int_part != 0 else "0"

    # 转换小数部分
    if frac_part == 0:
        return int_str
    # import string; chars = string.digits + string.ascii_lowercase
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    frac_str = ""
    temp = frac_part
    """      # 0.abc.... 十进制表示小数
    十进制小数 = a/10 + b/100 + c/1000 + ... 乘以10 ==> a + b/10 + c/100 + ... 取整数部分得到 a 然后减掉整数部分a 类似操作得到 b,c ....就是0.abc...
    36进制小数 = a/36 + b/36² + c/36³ + ...
    0.2 × 36 = 7.2   → 整数 7 ('7')
    0.2 × 36 = 7.2   → 整数 7 ('7')
    ... 无限循环
    结果: 0.2(10) = 0.777777...(36) 无限位
    能否精确表示 = 分母是否能写成 2^m × 3^n 的形式,因为 36 = 2² × 3²
    二进制: 1/2 1/4 1/8 1/(2^n)均能精确表示，其余不能.
    """
    for _ in range(precision):
        temp *= 36      # 乘 k 取整法 不逆
        digit = int(temp)
        frac_str += chars[digit]
        temp -= digit
        if temp == 0:
            break

    return f"{int_str}.{frac_str}"
# s = (float_to_base36(random.random())[2:] + float_to_base36(random.random())[2:])
# print(s, len(s))
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "range": "bytes=0-255",
    "referer": "https://spiderbuf.cn/web-scraping-practice/web-scraping-practice-c13",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "x-timestamp": str(int(time.time() *1000)),
    "x-token": (float_to_base36(random.random())[2:] + float_to_base36(random.random())[2:])
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775305179$o23$g1$t1775305306$j53$l0$h0"
}
all_data_b64 = ""
url = "https://spiderbuf.cn/web-scraping-practice/web-scraping-practice-c13/api"
next = 0
while next != -1:
    response = requests.get(url, headers=headers, cookies=cookies)
    data_json = response.json()
    data = data_json["data"]
    next = data_json["next"]
    sign = data_json["sign"]
    token = data_json["token"]
    timestamp = str(int(time.time() * 1000))
    headers.update({"X-Timestamp": timestamp, "X-Token": token, "X-Sign":sign, "range":f"bytes={next}-{next+255}"})
    print(f"{next:4d}")
    all_data_b64 += data

all_data = base64.b64decode(all_data_b64).decode()
json_data = json.loads(all_data)
print(all_data)
df = pd.DataFrame(json_data, columns=["keyword", "cpc_usd", "monthly_search_volume", "competition", "industry", "source"])
df["CPC"] = df.apply(
    lambda row: js_xor(row["cpc_usd"], row["monthly_search_volume"]) / 100,
    axis=1
)
print(df.to_string(index=False))
print(f"cpc_usd列的平均值: {df['cpc_usd'].agg('mean'):.4f}")
print(f"CPC列的平均值: {df['CPC'].agg('mean'):.4f}")

