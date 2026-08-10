"""拦截器"""

import json
import base64
from curl_cffi import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(plain_text:str, key:str="$shanghaidianqi$", iv:str="2023050814260000"):
    padded_data = pad(plain_text.encode(), AES.block_size,style='pkcs7')
    return base64.b64encode(AES.new(key.encode(), AES.MODE_CBC, iv.encode()).encrypt(padded_data)).decode()


def aes_decrypt(encrypted:bytes, key:str="$shanghaidianqi$", iv:str="2023050814260000"):
    encrypted_bytes = base64.b64decode(encrypted)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    plaintext = cipher.decrypt(encrypted_bytes)
    plaintext = unpad(plaintext, AES.block_size, style='pkcs7')

    return plaintext.decode('utf-8')


def get_data(page_num):
    headers = {
        'accept': 'application/json',
        'authorization': 'null',
        'content-type': 'application/json;charset=UTF-8, application/json;charset=UTF-8',
        'origin': 'https://www.hfhuizhan.com',
        'referer': 'https://www.hfhuizhan.com/tenderNotice/tenderNotice',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    }
    plain_data = {
        "pageSize": 5, # 每页5条记录
        "pageNum": page_num, 
        "platName": "website",
        "typeName": "中标结果公告"   # "中标结果公告" "招采公告"
    }
    pp = json.dumps(plain_data, separators=(',',":"))
    json_data = {
        'data': aes_encrypt(pp)
    }

    response = requests.post(
        'https://www.hfhuizhan.com/prod-api/hfhz-pavilion/back/pto/pavilion/listPagePavilionNews',
        headers=headers,
        json=json_data,
    )

    data = json.loads(aes_decrypt(response.content))['data']
    pages = data['pages'] # 总页数
    records = data['records']
    print(f"总页数: {pages}".center(100, '-'))
    # print(records)
    result = []
    for record in records:
        res = {}
        res["createdTime"] = record['createdTime']
        res["title"] = record['title']
        res['publisher'] = record['publisher']
        res['publishTime'] = record['publishTime']
        res['id'] = record['id']

        result.append(res)
    print(result)


def get_detial_data(id):
    pp = f"/prod-api/hfhz-pavilion/back/pto/pavilion/getNewDetailByIdV2=undefined&id={id}&platName=website"
    headers = {
        'authorization': 'null',
        'content-type': 'application/json;charset=UTF-8',
        'referer': 'https://www.hfhuizhan.com/tenderNotice/tenderNotice',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    }
    params = {
        'data': aes_encrypt(pp)
    }
    response = requests.get(
        'https://www.hfhuizhan.com/prod-api/hfhz-pavilion/back/pto/pavilion/getNewDetailByIdV2',
        params=params,
        headers=headers,
    )
    daat = json.loads(aes_decrypt(response.content))['data']
    return daat

if __name__ == "__main__":
    get_data(3)
    detial = get_detial_data("2052552438473269250")
    print(detial)