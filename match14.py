import time 
import base64
import subprocess
from curl_cffi import requests
import execjs

with open('./js/match14.js', 'r', encoding='utf-8') as fr:
    core_js = fr.read()
with open('./js/env14.js', 'r', encoding='utf-8') as fr:
    env_js = fr.read()

def get_mz():
    z = "Mozilla,Netscape,5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36,[object NetworkInformation],true,,[object Geolocation],12,zh-CN,zh-CN,zh,0,[object MediaCapabilities],[object MediaSession],[object MimeTypeArray],true,[object Permissions],Win32,[object PluginArray],Gecko,20030107,[object UserActivation],Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36,Google Inc.,,[object DeprecatedStorageQuota],[object DeprecatedStorageQuota],816,0,0,1536,24,864,[object ScreenOrientation],24,1536,[object DOMStringList],function assign() { [native code] },,match.yuanrenxue.cn,match.yuanrenxue.cn,https://match.yuanrenxue.cn/match/14,https://match.yuanrenxue.cn,/match/14,,https:,function reload() { [native code] },function replace() { [native code] },,function toString() { [native code] },function valueOf() { [native code] }"
    mz = base64.b64encode(z.encode()).decode()
    return mz


headers = {
    "referer": "https://match.yuanrenxue.cn/match/14",
    "user-agent": "yuanrenxue",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "1i5v0k8r6a43wlsyiawqngaitay2n0xi",
    "mz": get_mz(),
}
session = requests.Session(headers=headers, cookies=cookies)


total = 0
for page_num in range(1,3):
    url = "https://match.yuanrenxue.cn/api2/14"
    v12v142 = session.get(url).content.decode()
    js_code = env_js + v12v142 + core_js
    ctx = execjs.compile(js_code)
    m = ctx.call('sp', page_num)
    print(m)
    session.cookies.update({'m': m})

    url = "https://match.yuanrenxue.cn/api/question/14"
    params = {
        "page": str(page_num),
        "pageSize": "10",
        "kw": ""
    }
    resp = session.get(url, params=params)
    total += sum(resp.json()["data"])
    print(resp.json()["data"])


