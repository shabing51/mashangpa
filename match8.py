from curl_cffi import requests
from io import BytesIO
from PIL import Image
import ddddocr
import base64
import json
import time
import re
import random


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
        
        # OCR纠错映射
        self.ocr_mapping = {
            "o": "0", "O": "0", "Ｏ": "0",
            "l": "1", "I": "1", "i": "1", "|": "1",
            "z": "2", "Z": "2",
            "b": "6", "B": "8",
            "g": "9", "q": "9",
            "s": "5", "S": "5",
            "t": "7", "T": "7",
        }

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
        match = re.search("(?<=base64,).*", data["image"])
        if not match:
            raise Exception("图片base64解析失败")
        
        img_bytes = base64.b64decode(match.group())
        return Image.open(BytesIO(img_bytes))

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
                    (col+1) * cell_w,
                    (row+1) * cell_h
                )
                crop = img.crop(box)
                yield (row, col, crop)

    def correct_ocr_result(self, char):
        """
        OCR结果纠错
        """
        # 去除空白字符
        char = str(char).strip()
        
        # 使用映射表纠错
        if char in self.ocr_mapping:
            return self.ocr_mapping[char]
        
        # 如果是单个字符且可能是误识别，保持原样
        if len(char) == 1:
            return char
        
        # 如果识别出多个字符，取第一个
        if len(char) > 1:
            return char[0]
        
        return char

    def recognize(self, img):
        """
        OCR识别九宫格
        """
        result = {}

        for row, col, crop in self.split_image(img):
            char = self.ocr.classification(crop)
            char = self.correct_ocr_result(char)
            
            # 添加随机偏移，模拟人工点击
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)
            
            result[char] = {
                "x": col * 100 + 50 + offset_x,
                "y": row * 100 + 50 + offset_y
            }
            
            print(f"位置({row},{col}): 识别为 '{char}'")

        return result

    def verify(self, captcha_id, clicks):
        """
        验证验证码
        """
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://match.yuanrenxue.cn",
            "referer": "https://match.yuanrenxue.cn/match/8",
            "user-agent": "yuanrenxue",
            "x-requested-with": "XMLHttpRequest",
        }
        self.session.headers.update(headers)

        data = {
            "captcha_id": str(captcha_id),
            "clicks": json.dumps(clicks, separators=(",", ":"))
        }
        resp = self.session.post(self.verify_url, data=data)
        return resp.json()

    def solve_captcha(self, max_retries=3):
        """
        解决验证码，带重试机制
        """
        for attempt in range(max_retries):
            try:
                print(f"\n第 {attempt + 1} 次尝试解决验证码...")
                
                data = self.get_captcha()
                captcha_id = data["id"]
                targets = data["targets"]
                
                print(f"目标文字: {targets}")
                
                img = self.base64_to_image(data)
                classification = self.recognize(img)
                
                print(f"识别结果: {list(classification.keys())}")
                
                # 构建点击坐标
                clicks = []
                missing_chars = []
                
                for char in targets:
                    if char in classification:
                        clicks.append(classification[char])
                    else:
                        missing_chars.append(char)
                
                if missing_chars:
                    print(f"警告: 未识别到文字: {missing_chars}")
                    if attempt < max_retries - 1:
                        print("重试中...")
                        time.sleep(random.uniform(0.5, 1.5))
                        continue
                
                if len(clicks) != len(targets):
                    print(f"点击数量不匹配: 需要{len(targets)}个, 实际{len(clicks)}个")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(0.5, 1.5))
                        continue
                
                # 验证
                result = self.verify(captcha_id, clicks)
                print(f"验证结果: {result}")
                
                if result.get("ok"):
                    return result
                else:
                    print(f"验证失败: {result.get('msg', '未知错误')}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(0.5, 1.5))
                        
            except Exception as e:
                print(f"异常: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(1, 2))
        
        raise Exception("验证码解决失败，已达到最大重试次数")

    def get_data_by_page(self, page_num=1):
        """
        获取指定页的数据
        """
        params = {
            "page": str(page_num),
            "pageSize": "10"
        }
        resp = self.session.get(self.data_url, params=params)
        return resp.json()
    
    def get_all_data(self):
        """
        获取所有页的数据
        """
        total_sum = 0
        
        for page_num in range(1, 6):
            print(f"\n{'='*50}")
            print(f"正在处理第 {page_num} 页...")
            print('='*50)
            
            # 解决验证码
            result = self.solve_captcha()
            print(f"验证码结果: {result}")
            
            # 获取数据
            data = self.get_data_by_page(page_num=page_num)
            page_data = data.get("data", [])
            page_sum = sum(page_data)
            total_sum += page_sum
            
            print(f"第 {page_num} 页数据: {page_data}")
            print(f"第 {page_num} 页总和: {page_sum}")
            print(f"累计总和: {total_sum}")
            
            # 页面间延时
            if page_num < 5:
                time.sleep(random.uniform(1, 2))
        
        return total_sum


if __name__ == "__main__":
    spider = YuanRenXueCaptcha()
    
    try:
        total = spider.get_all_data()
        print(f"\n{'='*50}")
        print(f"最终结果 - 总和为: {total}")
        print('='*50)
    except Exception as e:
        print(f"程序执行失败: {e}")