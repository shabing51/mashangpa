import random
import execjs
import hashlib
import requests
import time, json
import pandas as pd
import string, base64
from urllib.parse import quote
"""
    双重加密：密钥本身也被加密传输
    动态签名：每次请求的 key 和 t2 都不同
    Cookie 验证：__check_once 存储 key 用于服务端验证
    反调试：禁止 F12 和右键菜单
    反自动化：检测 webdriver 和 cdc_ 属性
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# with open('C12_.js', "r", encoding='utf-8') as f:
#     js_code = f.read()
# ctx = execjs.compile(js_code)


# 获取实时汇率
def get_eur_usd_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['rates']['USD']
    except:
        return 1.09  # 默认汇率

eur_to_usd = get_eur_usd_rate()
print(f"当前汇率: 1 EUR = {eur_to_usd} USD")

def decrypt(key_str: str, ciphertext_b64: str) -> str:
    """AES-CBC 解密"""
    combined = base64.b64decode(ciphertext_b64)
    iv = combined[:16]
    ciphertext = combined[16:]
    key = key_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded, AES.block_size)
    return plaintext.decode('utf-8')

# 1. 生成随机 key
characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
key = ''.join(random.choice(characters) for _ in range(16))
print(f"Key: {key}")

# 2. 生成签名
t2 = int(time.time())
md5_hex = hashlib.md5(f"{t2}{key}".encode()).hexdigest()

# 3. 请求数据
session = requests.Session()
session.cookies.clear(), session.cookies.set("__check_once", quote(key, safe=''))
session.headers.clear()
session.headers.update({
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "referer": "https://spiderbuf.cn/web-scraping-practice/web-scraping-practice-js-reverse-c12"
})

resp = session.get(
    "https://spiderbuf.cn/web-scraping-practice/web-scraping-practice-js-reverse-c12/api",
    params={"q": md5_hex, "t": t2}
).json()
print(resp)
# 4. 两步解密
# 第一步: 用原始 key 解密 b，得到真正的密钥
real_key = decrypt(key, resp['b'])
print(f"Real Key: {real_key}")
# r_Key_by_js = ctx.call('decrypt', key, resp['b'])
# print(f"JS: {r_Key_by_js}")
# 第二步: 用真正的密钥解密 a，得到商品数据
data_json_str = decrypt(real_key, resp['a'])
products = json.loads(data_json_str)
# data_json_str_js = ctx.call('decrypt', r_Key_by_js, resp['a'])
df = pd.DataFrame(products)
# table = df[df['memory'].isin(['24GB', '32GB'])]
# table = df[(df['memory'] == '24GB') | (df['memory'] == '32GB')]
table = df.query("memory in ['24GB','32GB']")
print(df.to_string())
print("+"*100)

table['price_usd'] = table.apply(
    lambda row: row['price'] if row['currency'] == 'USD' else row['price'] * eur_to_usd,
    axis=1
)
print(table.to_string(index=False))
print(table['price_usd'].agg(['mean', 'sum']))
print(table['price'].agg(['mean', 'sum']))






"""
┌─────────────────────────────────────────────────────────────┐
│                    页面加载 (Page Load)                       │
├─────────────────────────────────────────────────────────────┤
│  1. 反调试检测 (F12, Ctrl+Shift+I, 右键菜单)                   │
│  2. 反自动化检测 (navigator.webdriver, cdc_ 属性)             │
│  3. 生成随机 key (16位，A-Za-z0-9)                            │
│  4. 生成时间戳 t1, t2 和 MD5 签名                              │
│  5. 设置 Cookie: __check_once = encodeURIComponent(key)      │
│  6. 发送 API 请求                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    第一次 API 响应                            │
│  { "a": "加密的商品数据", "b": "加密的密钥" }                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    解密流程                                   │
│  1. 用原始 key 解密 b → 得到 real_key (16位)                   │
│  2. 用 real_key 解密 a → 得到商品 JSON 数据                     │
│  3. 渲染 HTML 表格                                            │
└─────────────────────────────────────────────────────────────┘
"""