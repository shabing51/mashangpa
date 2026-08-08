import base64
import binascii
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

import time
import json
import hashlib
import requests

def get_headers_and_x():
    ts = str(int(time.time()*1000))
    _ = f"xialuo{ts}"
    m = hashlib.md5(_.encode('utf-8')).hexdigest()
    x = hashlib.sha256(f"{m}xxoo".encode('utf-8')).hexdigest()
    return {"ts": ts, "m": m,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
            "refere":"https://www.mashangpa.com/problem-detail/7/"
    }, x


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

if __name__ == "__main__":
    print(f"".center(62, '='))
    total = 0
    key = 'xxxxxxxxoooooooo'
    iv  = "0123456789ABCDEF"

    session = requests.Session()
    session.headers.clear(); session.cookies.clear()
    session.cookies.update(
        {
            "sessionid": '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs'
        }
    )

    for page_num in range(1,21):
        headers, x = get_headers_and_x()
        session.headers.update(headers)

        params = {
            "page": page_num,
            "x": x,
        }
        resp = session.get(("https://www.mashangpa.com"
                        "/api/problem-detail/7/data/"), 
                           params=params)
        cipher_text = resp.json().get("r")
        res = json.loads(aes_cbc_decrypt(
            ciphertext=cipher_text, key=key, iv=iv
            )).get('current_array')
        
        print(f"{page_num:02d}\t{res}")
        total += sum(res)

    print(f"20页数据的和: {total} ".center(56, '='))