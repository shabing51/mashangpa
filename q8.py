import time
import base64
import requests

def OOOoO(s):
 """循环位移和异或运算对每个字符独立加密"""
 result_chars = []

 # 遍历每个字符
 for ch in s:
     v = ord(ch)
     v = ((v << 3) | (v >> 5)) & 0xFF
     v ^= 0x5A
     v = ((v << 2) | (v >> 6)) & 0xFF
     v ^= 0x3F   # 0x3F = 3 * 16 + 15 = 63
     v %= 0x100  # 0x100 = 16^2 = 256
     result_chars.append(chr(v))

 # 转十六进制
 return ''.join(f'{ord(c):02x}' for c in result_chars)


def OOOoOo(str1, key):
    """使用密钥循环加法，类似维吉尼亚密码"""
    result = []

    for i, ch in enumerate(str1):
        # 获取 str2 对应位置的字符（循环）
        key_char = key[i % len(key)] if key else ''
        key_val = ord(key_char) if key_char else 0

        # 加密：加法后取模 256
        encrypted_val = (ord(ch) + key_val) % 256

        result.append(f'{encrypted_val:02x}')

    return ''.join(result)

def decode_OOOoOo(hex_str, str2):
    """解密函数"""
    # 十六进制转字符串
    encrypted = bytes.fromhex(hex_str).decode('latin-1')
    result = []

    for i, ch in enumerate(encrypted):
        key_char = str2[i % len(str2)]
        key_val = ord(key_char)
        # 解密：减去密钥值
        decrypted_val = (ord(ch) - key_val) % 256
        result.append(chr(decrypted_val))

    return ''.join(result)  # #


if __name__ == '__main__':
    print(f"".center(62, '='))
    total = 0
    url = "https://www.mashangpa.com/api/problem-detail/8/data/"
    session = requests.Session()
    session.headers.clear(); session.cookies.clear() # 先清理一下header是个好习惯(某些网站会检测请求头顺序,这里不会)
    session.cookies.update(
        {
            "sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs"
        }
    ) # sessionid两个周后过期
    for pageNumber in range(1, 21):

        data = {
            "page": pageNumber,
        }

        ts = str(int(time.time() * 1000))
        s = OOOoO('xoxoxoxo' + ts)

        t = base64.b64encode(ts.encode('utf-8')).decode()
        m = OOOoOo('oooooo' + ts + str(pageNumber), 'oooooo')
        headers = {
            "t": t,
            "m": m,
        }

        session.cookies.update({"s": s})
        resp = session.post(url, headers=headers, json=data).json()
        current_array = resp.get("current_array")

        print(f"第{pageNumber:02d}页数据: {current_array}")

        total += sum(current_array)

    print(f"20页数据的和: {total} ".center(56, '='))

