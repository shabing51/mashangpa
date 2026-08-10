from curl_cffi import requests
from io import BytesIO
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import ddddocr
ocr = ddddocr.DdddOcr(show_ad=False)

def aes_encrypt(plain_text:str, key:str="397151C04723421F"):
    padded_data = pad(plain_text.encode(), AES.block_size,style='pkcs7')
    return AES.new(key.encode(), AES.MODE_ECB).encrypt(padded_data).hex()

def get_code_bytes():
    import random
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'referer': 'https://www.jisilu.cn/login/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    }
    random_num = random.randint(1000, 9999) #[1000, 9999]
    response = requests.get(f'https://www.jisilu.cn/account/captcha/{random_num}', headers=headers)
    return response.content, dict(response.cookies)

def save_code_img(content):
    with open("./aef/jsl.png", 'wb') as fr:
        fr.write(content)

def recognize_the_verification_code(content):
    buffer = BytesIO(content)
    ocr_res = ocr.classification(buffer.getvalue())
    print(f"{ocr_res=}")
    return ocr_res

def check_code_verify(code_verify, cookie_dict):
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.jisilu.cn',
        'referer': 'https://www.jisilu.cn/login/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'code_verify': code_verify,
    }
    response = requests.post('https://www.jisilu.cn/webapi/account/check_code_verify/', cookies=cookie_dict, headers=headers, data=data)
    if (response.json().get("code") == 200):
        return True
    
    return False

def login_process(code_verify, cookie_dict, phone_num='18888888888',pwd="123456"):
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.jisilu.cn',
        'referer': 'https://www.jisilu.cn/login/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'return_url': '/',
        'user_name': aes_encrypt(phone_num),
        'password': aes_encrypt(pwd),
        'auto_login': '1',
        'aes': '1',
        'code_verify': code_verify,
    }

    response = requests.post('https://www.jisilu.cn/webapi/account/login_process/', 
                             cookies=cookie_dict, 
                             headers=headers, 
                             data=data)

    return response.json()

def main():
    content, cookie_dict = get_code_bytes()
    # save_code_img(content=content) # 可选
    code_verify = recognize_the_verification_code(content=content)
    ok = check_code_verify(code_verify, cookie_dict)
    if not ok:
        raise ValueError("验证码识别错误")
    data = login_process(code_verify, cookie_dict)
    print(data)

if __name__ == "__main__":
    main()