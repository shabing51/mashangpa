import time
import json
import requests

import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def my_aes_encrypt(plaintext: str, key="jo8j9wGw%6HbxfFn", iv="0123456789ABCDEF"):
    """AES-128 CBC模式"""
    # 确保key是16字节
    key_bytes = key.encode('utf-8') if isinstance(key, str) else key
    if len(key_bytes) != 16:
        raise ValueError(f"Key必须是16字节, 当前是{len(key_bytes)}字节")

    # 确保iv是16字节
    iv_bytes = iv.encode('utf-8') if isinstance(iv, str) else iv
    if len(iv_bytes) != 16:
        raise ValueError(f"IV必须是16字节, 当前是{len(iv_bytes)}字节")

    # PKCS7填充
    plaintext_bytes = plaintext.encode('utf-8')
    padded_data = pad(plaintext_bytes, AES.block_size)

    # 加密
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    ciphertext = cipher.encrypt(padded_data)

    # 返回十六进制字符串
    return binascii.hexlify(ciphertext).decode()

def get_data_by_page(page_num):
    _ts = int(time.time() * 1000)
    data_dict = {
        "page": page_num,
        "_ts": _ts
    }
    data_str = json.dumps(data_dict)
    xl = my_aes_encrypt(data_str)
    data = {"xl": xl}

    response = requests.post(url, json=data, cookies=cookies)
    current_array = response.json().get("current_array")
    print(f"第{page_num:2d}页数据: {current_array}")
    return current_array


if __name__ == '__main__':
    print(f"".center(62, '='))
    total = 0 
    url = "https://www.mashangpa.com/api/problem-detail/5/data/"
    cookies = { ##需要更换 sessionid
        'sessionid': '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs',
    }
    headers = {
        'pragma': 'no-cache',
        'referer': 'https://www.mashangpa.com/problem-detail/5/',
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/151.0.0.0 Safari/537.36'),
    }
    
    for ii in range(1,21):
        current_array = get_data_by_page(ii)
        total += sum(current_array)

    print(f"20页数据的和: {total} ".center(56, '='))