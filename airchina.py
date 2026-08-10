from curl_cffi import requests
import json
import subprocess

params = subprocess.run(["node", "yrx/airchina.js"], capture_output=True, text=True).stdout.strip()


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.airchina.com.cn",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.airchina.com.cn/flight/oneway/pek-ckg/2026-08-28",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sgm-context": "124131261513124880;124131261513124880",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-device-token": "tak01j5DYI2WYUKANYZKVNEAMEDDKD4MRIABVCOF3ET2B5KPLXM5QVXYETJCAG3QROXIQ54IWNV6GTTH6UJYKOB5LOOKTYBEJNGFJGUNO3B42HQR5OHHSZULAUDUXLYVTNFDTYKVLZ4XCJIYQSEMOWTAJJ622ZYD4Q",
    "x-locale": "zh-CN"
}
cookies = {
    "HWWAFSESTIME": "1785749664172",
    "HWWAFSESID": "c34c982a085e838b06",
    "_gcl_au": "1.1.2070989499.1785749669",
    "arialoadData": "true",
    "_ga": "GA1.1.1920728888.1785749670",
    "ariawapChangeViewPort": "false",
    "TKAEQLILOIB0YIMO": "tak01j5DYI2WYUKANYZKVNEAMEDDKD4MRIABVCOF3ET2B5KPLXM5QVXYETJCAG3QROXIQ54IWNV6GTTH6UJYKOB5LOOKTYBEJNGFJGUNO3B42HQR5OHHSZULAUDUXLYVTNFDTYKVLZ4XCJIYQSEMOWTAJJ622ZYD4Q",
    "ariauseGraymode": "false",
    "ariaappid": "1cea560ed256bea7ae52761bd9042164",
    "_ga_CGYVD7S4G4": "GS2.1.s1785756235$o2$g1$t1785757731$j60$l0$h0"
}
url = "https://www.airchina.com.cn/gateway/api/flight/list"
data = {
    "params": params,
    "RequestParameterEncryptionIdentificationBit": True
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.json())
