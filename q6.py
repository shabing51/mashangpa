import time
import json
import hashlib
import requests

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import binascii

def aes_cbc_decrypt(ciphertext, key="xxxxxxxxoooooooo", iv="0123456789ABCDEF"):
    """
    AES-CBC模式解密, PKCS7填充
    """
    # 确保key和iv是bytes类型
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')

    # 处理密文(可能是base64或hex格式) 这里是hex格式
    if isinstance(ciphertext, str):
        # 尝试判断编码格式
        if len(ciphertext) % 2 == 0 and all(c in '0123456789abcdefABCDEF' for c in ciphertext):
            ciphertext = binascii.unhexlify(ciphertext)  # hex格式
        else:
            ciphertext = base64.b64decode(ciphertext)  # base64格式

    # 创建解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密并去除填充
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, AES.block_size)

    return decrypted.decode('utf-8')

def get_headers():
    ttt = str(int(time.time() * 1000))
    s = hashlib.md5(f"sssssbbbbb{ttt}".encode("utf-8")).hexdigest()
    headers = {
        "s": s,
        "tt": ttt
    }
    return headers

def get_data_by_page(page_nu):
    headers = get_headers()
    params = {
        "page": page_nu
    }
    resp = requests.get(base_url, headers=headers, cookies=cookies, params=params)
    cipher_text = resp.json().get('t')
    current_array = json.loads(aes_cbc_decrypt(cipher_text)).get('current_array')
    print(f"第{page_nu:02d}页数据: {current_array}")
    return current_array


if __name__ == '__main__':
    print(f"".center(62, '='))
    total = 0
    base_url = ("https://www.mashangpa.com"
            "/api/problem-detail/6/data/")
    cookies = { ##需要更换 sessionid
            'sessionid': '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs',
    }
    headers = {
        'pragma': 'no-cache',
        'referer': 'https://www.mashangpa.com/problem-detail/6/',
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/151.0.0.0 Safari/537.36'),
    }

    for page_num in range(1, 21):
        current_array = get_data_by_page(page_num)
        total += sum(current_array)

    print(f"20页数据的和: {total} ".center(56, '='))



