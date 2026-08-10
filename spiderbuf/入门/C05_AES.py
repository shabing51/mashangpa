from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
from hashlib import md5
import pandas as pd
import subprocess
import requests
import base64
import json
import re
import os

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16):
    """
    模拟 OpenSSL 的 EVP_BytesToKey 函数，用于从密码和盐值派生密钥和 IV。
    这是 CryptoJS 使用字符串密码时的核心派生算法。
    """
    dtot = b''
    final_key_iv = b''
    while len(final_key_iv) < key_len + iv_len:
        dtot = md5(dtot + password + salt).digest()
        final_key_iv += dtot
    key = final_key_iv[:key_len]
    iv = final_key_iv[key_len:key_len+iv_len]
    return key, iv

def aes_cbc_decrypt(_ciphertext_b64, password):
    # 1. Base64 解码
    raw_data = base64.b64decode(_ciphertext_b64)
    # 2. 检查 OpenSSL 格式的头部，并提取盐值
    # CryptoJS 生成的密文格式是: "Salted__" (8字节) + Salt (8字节) + 实际密文
    if raw_data[:8] != b'Salted__':
        raise ValueError("密文不是标准的 OpenSSL 格式，无法使用密码派生方式解密")
    salt = raw_data[8:16]  # 提取盐值
    ciphertext = raw_data[16:]  # 剩余部分是真正的密文

    # 3. 使用 EVP_BytesToKey 从密码和盐值派生 AES-256 的密钥 (32字节) 和 IV (16字节)
    key, iv = evp_bytes_to_key(password.encode('utf-8'), salt, key_len=32, iv_len=16)
    # 1.创建加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    # 2.解密
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    # 去除填充,得到明文decrypted
    pad_len = decrypted_padded[-1] # pkcs7
    decrypted = decrypted_padded[:-pad_len]

    return decrypted.decode('utf-8')

if __name__ == '__main__':
    # 1.发请求，拿到AES加密后的数据然后解密
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1",
        "referer": "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c05",
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
        "_ga_7B42BKG1QE": "GS2.1.s1775267779$o17$g1$t1775268052$j60$l0$h0"
    }
    url = "https://spiderbuf.cn/static/js/c05.min.js"
    response = requests.get(url, headers=headers, cookies=cookies)
    cipher_text = re.findall(r"XQyP\',\'(.*?)\',\'", response.text)[0]
    # print(cipher_text)
    # 2.解密，获得明文
    # 2.1 python
    decrypted_text = aes_cbc_decrypt(cipher_text, "mySecretKey123")
    # 2.2 js
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['EXECJS_RUNTIME'] = 'Node'
    with open("C05_AES.js", "r", encoding="utf-8") as f:
        js_code = f.read()
    try:
        # 执行 Node.js
        result = subprocess.run(
            ['node', '-e', js_code, cipher_text],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        # print(result)
        plain_text = result.stdout.strip()
        print("plain_text", plain_text)
    except subprocess.TimeoutExpired:
        pass

    data_list = json.loads(decrypted_text).get("flights")
    # print(data_list)
    df = pd.DataFrame(data_list, columns=['from', 'to', 'price'])
    print(df['price'].agg('mean'))  ################# ##########$$$$$$$
    print(df.to_string(index=False))


