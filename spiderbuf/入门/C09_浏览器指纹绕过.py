import base64
import requests
import time,json
import pandas as pd
import hmac,hashlib
from playwright.sync_api import sync_playwright


def get_fingerprint_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 注入 CryptoJS
        page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js")

        # 执行指纹函数
        fingerprint = page.evaluate('''
            () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.fillStyle = '#f60';
                ctx.font = '14px Arial';
                ctx.fillRect(125, 1, 62, 20);
                ctx.fillStyle = '#069';
                ctx.font = '14px Wingdings';
                ctx.fillText('RSAMD5DES', 2, 15);
                const canvasData = canvas.toDataURL();
                return CryptoJS.SHA256(canvasData + navigator.userAgent).toString();
            }  
        ''')
        browser.close()
        return fingerprint


session = requests.Session()

headers = {
    "referer": "https://spiderbuf.cn/web-scraping-practices/8?order=rating",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}

session.headers.clear(),session.cookies.clear()
session.headers.update(headers)

url = "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c09"
response = session.get(url)
# print(session.cookies) # <RequestsCookieJar[<Cookie _token_c09=b06da254820c0fc2f3b267be5573dc331dc307e3f89708433a8c6d3f67fedb14 for .spiderbuf.cn/>]>
# print(response.headers.get('x-token'))
# print(response.headers.get('Set-Cookie'))
# fp = get_fingerprint_playwright()

fp = 'fd6a14af844de52b9ac10e521721ab55f1b7f1e081a5cbe0ce2811dbcd6eaa43'
session.headers.update({"x-client-id": fp, "referer": url})
t = session.cookies.get('_token_c09') # 参数弄错了封 IP 5mins

tt = int(time.time())

msg = f"{fp}{tt}{t}"

s = hmac.new(bytes(t, encoding="utf-8"), msg.encode('utf-8'), hashlib.sha256).digest()
s_b64 = base64.b64encode(s).decode()
print("s_b64", s_b64)
data = {
    "tt":tt,
    "s": s_b64,
}
print("data", data)
data = json.dumps(data, separators=(',', ':'))
resp = session.post(url, data=data)
if resp.status_code == 200:
    json_data = resp.json()
    df = pd.DataFrame.from_dict(json_data)
    df['CPC'] = (df['cpc_usd'] ^ df['monthly_search_volume']) / 100
    print(df.to_string())
    print("CPC均值: ",df["CPC"].agg('mean'))
else:
    print(resp.text)
