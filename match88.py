from curl_cffi import requests
from io import BytesIO
from PIL import Image
import ddddocr
import base64
import json
import time
import re


class YuanRenXueCaptcha:

    def __init__(self):
        self.img_url = "https://match.yuanrenxue.cn/api2/8"
        self.verify_url = "https://match.yuanrenxue.cn/api2/8"
        self.data_url = "https://match.yuanrenxue.cn/api/question/8"
        self.cookies = {
            "sessionid": "qcngxf1p24fbthxucr94o1std0qhdms8",
        }
        self.headers = {
            "referer": "https://match.yuanrenxue.cn/match/8",
            "user-agent": "yuanrenxue",
            "x-requested-with": "XMLHttpRequest"
        }
        self.session = requests.Session(
            headers=self.headers,
            cookies=self.cookies
        )
        self.ocr = ddddocr.DdddOcr(
            show_ad=False
        )

    def get_captcha(self):
        """
        获取验证码图片、id、targets
        """
        params = {
            "t": str(int(time.time()*1000))
        }
        data = self.session.get(
            self.img_url,
            params=params
        ).json()

        return data

    def base64_to_image(self, data):
        """
        base64 转图片
        """
        match = re.search("(?<=base64,).*",data["image"])

        if not match:
            raise Exception(
                "图片base64解析失败"
            )

        img_bytes = base64.b64decode(
            match.group()
        )
        return Image.open(
            BytesIO(img_bytes)
        )

    def split_image(self, img):
        """
        九宫格切割
        """
        w, h = img.size
        cell_w = w // 3
        cell_h = h // 3

        for row in range(3):
            for col in range(3):
                box = (
                    col * cell_w,
                    row * cell_h,
                    (col+1)*cell_w,
                    (row+1)*cell_h
                )
                crop = img.crop(box)
                yield (row,col,crop)


    def recognize(self, img):
        """
        OCR识别九宫格
        """
        result = {}

        for row, col, crop in self.split_image(img):
            char = self.ocr.classification(crop)
            # OCR纠错
            mapping = {
                "o": "0",
                "O": "0",
                "l": "1",
                "I": "1"
            }
            char = mapping.get(str(char), char)

            result[char] = {
                "x": col*100+50,
                "y": row*100+50
            }

        return result


    def verify(self, captcha_id, clicks):
        headers = {
            "content-type":
                "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://match.yuanrenxue.cn",
            "referer":"https://match.yuanrenxue.cn/match/8",
            "user-agent":"yuanrenxue",
            "x-requested-with":"XMLHttpRequest",
        }
        self.session.headers.update(headers)

        data = {
            "captcha_id": str(captcha_id),
            "clicks": json.dumps(
                clicks,
                separators=(",", ":")
            )
        }
        resp = self.session.post(
            self.verify_url,
            data=data
        )
        return resp.json()


    def solve_captcha(self):
        data = self.get_captcha()

        captcha_id = data["id"]
        targets = data["targets"]

        img = self.base64_to_image(data)
        classification = self.recognize(img)
        print('targets: ', targets)
        print("classification: ", classification)
        clicks = []
        for char in targets:
            clicks.append(classification[char])
        return self.verify(captcha_id, clicks)

    def get_data_by_page(self, page_num=1):
        params = {
            "page": str(page_num),
            "pageSize": "10"
        }
        resp = self.session.get(
            self.data_url,
            params=params
        )
        return resp.json()
    
    def get_all_data(self):
        total_ = 0
        for page_num in range(1,6):
            result = self.solve_captcha()
            print(result)
            
            data = self.get_data_by_page(page_num=page_num)
            print(data)
            total_ = total_ + sum(data["data"])
        return total_

if __name__ == "__main__":
    spider = YuanRenXueCaptcha()

    total = spider.get_all_data()
    print(f"Total is {total}")