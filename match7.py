import io
import base64
import ddddocr
# import paddleocr  # pip install paddleocr
# # 初始化 OCR（只需一次）
# ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')  # 或 'ch'
from curl_cffi import requests
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

URL = "https://match.yuanrenxue.cn/api/question/7"
ocr = ddddocr.DdddOcr(beta=True,show_ad=False)

def fetch_raw_data_font_by_page(session, page_num):
    params = {
        "page": str(page_num),
        "pageSize": "10",
        "kw": ""
    }
    dddd = session.get(URL, params=params).json()
    raw_data = dddd['data']
    woff_base64 = dddd['woff']
    font_bytes = base64.b64decode(woff_base64)

    return font_bytes, raw_data


def get_font_map(font_bytes, size=256):
    """
    生成字体字符映射表: HTML实体 -> OCR识别结果
    """
    result_map = {}

    # 1. 加载字体
    pil_font = ImageFont.truetype(io.BytesIO(font_bytes), int(size * 0.7))

    # 2. 获取字符映射表
    tt_font = TTFont(io.BytesIO(font_bytes))
    cmap = tt_font.getBestCmap()  # {unicode_code: glyph_name}

    for code, glyph in cmap.items():
        # 跳过不可打印字符
        if code < 0x20 or code == 0x7F:
            continue

        char = chr(code)

        # 3. 创建画布并绘制字符
        img = Image.new("L", (size, size), 255)  # 白底
        draw = ImageDraw.Draw(img)

        # 计算文字边界框
        bbox = draw.textbbox((0, 0), char, font=pil_font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # 居中坐标
        x = (size - w) // 2 - bbox[0]
        y = (size - h) // 2 - bbox[1]

        draw.text((x, y), char, fill=0, font=pil_font)  # 黑色文字

        # 4. 放大到 512x512（提高 OCR 识别率）
        img_resized = img.resize((512, 512), Image.Resampling.LANCZOS)

        # 5. 转为字节流
        bio = io.BytesIO()
        img_resized.save(bio, format="PNG")
        img_bytes = bio.getvalue()

        # 6. OCR 识别
        try:
            result = ocr.classification(img_bytes)
        except Exception as e:
            print(f"OCR 失败: {hex(code)} - {e}")
            result = ""

        print(f"{hex(code)} ({glyph}) => '{result}'")

        # 修正 o-->0
        result = "0" if result == 'o' else result

        # 7. 只保留数字识别结果
        if result.isdigit():
            html_entity = f"&#x{code:x}"
            result_map[html_entity] = result

    tt_font.close()
    return result_map

def main():
    headers = {
        "referer": "https://match.yuanrenxue.cn/match/7",
        "user-agent": "yuanrenxue",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "sessionid": "1i5v0k8r6a43wlsyiawqngaitay2n0xi",
    }
    session =requests.Session(headers=headers, cookies=cookies)

    total = 0
    for page_num in range(1,6):

        font_bytes, raw_data = \
        fetch_raw_data_font_by_page(session, page_num)

        font_map = get_font_map(font_bytes)
        # print(font_map)
        data = []
        for item in raw_data:
            for o, n in font_map.items():
                item = item.replace(o, n)

            data.append(int(item))
        print(f"第{page_num}页数据: {data}")
        total += sum(data)
        print("="*91)

    print(f"Total is {total}")
    print("="*91)
    return total

if __name__ == "__main__":
    print("="*91)
    main()
