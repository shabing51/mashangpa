from curl_cffi import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


def get_encrypted_data(page_num):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.swguancha.com',
        'Referer': 'https://www.swguancha.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'deviceType': '1',
    }
    json_data = {
        'size': 16,
        'current': page_num,
        'propertyCode': [
            'DISTRICT_PROP_GJ025_RJDQSCZZ',
            'DISTRICT_PROP_GJ117_NMSYGGQDCYYCLS',
            'DISTRICT_PROP_GJ001_NMHJRK',
        ],
        'dimensionTime': '2019',
        'levelType': 2,
    }

    response = requests.post('https://app.swguancha.com/client/v1/cPublic/consumer/baseInfo', headers=headers, json=json_data)
    response.raise_for_status()
    encrypted_data = response.content
    print(response.status_code)
    return encrypted_data

def aes_decrypt(encrypted, key='QV1f3nHn2qm7i3xrj3Y9K9imDdGTjTu9'):
    encrypted_bytes = base64.b64decode(encrypted)
    cipher = AES.new(key.encode(),AES.MODE_ECB)
    plaintext = cipher.decrypt(encrypted_bytes)
    plaintext = unpad(plaintext,AES.block_size,style='pkcs7')

    return plaintext.decode('utf-8')

def main():
    enc = get_encrypted_data(3) # page_num
    data = aes_decrypt(enc)
    print(data)


if __name__ == "__main__":
    main()
