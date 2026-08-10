import base64
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import ddddocr
import pandas as pd

"""
网页HTML
    │
    ▼
1. get_sprite_image() ──► 提取base64图片 ──► PIL Image对象
    │
    ▼
2. parse_css_mapping() ──► 提取CSS映射 ──► {'abcdef': (-90,0), ...}
    │
    ▼
3. extract_numbers_from_sprite() ──► 裁剪+OCR ──► {'abcdef': '0', 'cdefgh': '1', ...}
    │
    ▼
4. 遍历每个企业卡片
    │
    ├─ 找<h2> → 企业名称
    ├─ 找包含"排名"的<p> → 排名
    ├─ 找包含"CEO"的<p> → CEO
    ├─ 找包含"行业"的<p> → 行业
    └─ card.select('p:has(span.sprite) span.sprite') → 估值数字的span列表
                                                              │
                                                              ▼
                                               decode_sprite_text() → "39000"
    │
    ▼
5. 组装成DataFrame，保存CSV
"""

class SpriteCracker:
    """雪碧图反爬破解器"""

    def __init__(self):
        self.ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
        self.number_map = {}  # class名 -> 数字

    def get_sprite_image(self, soup):
        """从页面的style标签中精确获取雪碧图图片"""
        style_tags = soup.find_all('style')

        for style in style_tags:
            if not style.string:
                continue
            # 匹配 url('data:image/png;base64,xxxx') 或 url("data:image/png;base64,xxxx")
            match = re.search(r"url\(['\"]?(data:image/png;base64,[^)'\"]+)['\"]?\)", style.string)
            if match:
                img_url = match.group(1)
                if img_url.startswith('data:image'):
                    base64_data = img_url.split(',')[1]
                    image_bytes = base64.b64decode(base64_data)
                    return Image.open(BytesIO(image_bytes))
        return None

    def parse_css_mapping(self, soup):
        """解析CSS，获取每个class对应的背景位置"""
        style_tags = soup.find_all('style')
        mapping = {}

        for style in style_tags:
            if not style.string:
                continue
            # 匹配 .classname { background-position: -Xpx Ypx; }
            pattern = r'\.(\w+)\s*{[^}]*background-position:\s*(-?\d+)px\s+(-?\d+)px;'

            for match in re.finditer(pattern, style.string):
                class_name = match.group(1)
                x = int(match.group(2))
                y = int(match.group(3))
                mapping[class_name] = (x, y)

        return mapping

    def extract_numbers_from_sprite(self, sprite_img, css_mapping):
        """从雪碧图中提取每个class对应的数字"""
        # 从CSS中获取单个数字的尺寸
        # 方法：找到任意一个.sprite类的width和height
        digit_width = 10  # 默认值，实际会从CSS覆盖
        digit_height = 12  # 默认值

        number_map = {}

        for class_name, (x, y) in css_mapping.items():
            # 背景位置是负数，表示偏移
            left = abs(x)
            top = abs(y)
            right = left + digit_width
            bottom = top + digit_height

            # 边界检查
            if right > sprite_img.width or bottom > sprite_img.height:
                print(f"警告: {class_name} 裁剪区域超出图片边界")
                continue

            # 裁剪数字图片 # # 裁剪出单个数字图片 # (左, 上, 右, 下)
            box = (left, top, right, bottom)
            digit_img = sprite_img.crop(box)

            # 使用OCR识别数字
            img_bytes = BytesIO()
            digit_img.save(img_bytes, format='PNG')
            result = self.ocr.classification(img_bytes.getvalue())

            # 存储映射关系
            number_map[class_name] = result
            print(f"{class_name:10s} -> {result} (位置: {x}, {y})")

        return number_map

    def decode_sprite_text(self, spans, number_map):
        """解码雪碧图文本"""
        result = ""
        for span in spans:
            class_list = span.get('class', [])
            for cls in class_list:
                if cls in number_map and cls != 'sprite':
                    result += number_map[cls]
                    break
        return result

    def process_page(self, url):
        """处理整个页面"""
        # 1. 获取页面
        print("正在获取页面...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. 获取雪碧图
        print("正在解析雪碧图...")
        sprite_img = self.get_sprite_image(soup)
        if not sprite_img:
            print("未找到雪碧图")
            return None
        print(f"雪碧图尺寸: {sprite_img.size}")

        # 3. 解析CSS映射
        print("正在解析CSS映射...")
        css_mapping = self.parse_css_mapping(soup)
        print(f"找到 {len(css_mapping)} 个CSS类映射")
        for cls, pos in css_mapping.items():
            print(f"  {cls}: {pos}")

        # 4. 识别数字
        print("\n正在识别数字...")
        number_map = self.extract_numbers_from_sprite(sprite_img, css_mapping)

        # 5. 处理所有企业数据
        print("\n正在提取企业数据...")
        companies = []

        # 查找所有企业卡片
        cards = soup.find_all('div', class_='col-xs-6')

        for card in cards:
            # 企业名称
            name_tag = card.find('h2')
            name = name_tag.text.strip() if name_tag else "未知"

            # 排名
            rank_tag = card.find('p', string=re.compile('排名'))
            rank = rank_tag.text.split('：')[-1].strip() if rank_tag else "未知"

            # CEO
            ceo_tag = card.find('p', string=re.compile('CEO'))
            ceo = ceo_tag.text.split('：')[-1].strip() if ceo_tag else "未知"

            # 行业
            industry_tag = card.find('p', string=re.compile('行业'))
            industry = industry_tag.text.split('：')[-1].strip() if industry_tag else "未知"

            # 企业估值（使用雪碧图）
            valuation_spans = card.select('p:has(span.sprite) span.sprite')
            valuation = self.decode_sprite_text(valuation_spans, number_map)

            companies.append({
                '企业名称': name,
                '排名': rank,
                '企业估值(亿元)': valuation,
                'CEO': ceo,
                '行业': industry
            })

            print(f"{name}: {valuation}亿元")

        return companies


def main():
    """主函数"""
    url = "https://spiderbuf.cn/web-scraping-practice/css-sprites"

    print("=" * 60)
    print("开始破解雪碧图反爬")
    print("=" * 60)

    cracker = SpriteCracker()
    data = cracker.process_page(url)

    if data:
        # 转换为DataFrame
        df = pd.DataFrame(data)

        print("\n" + "=" * 60)
        print("提取结果:")
        print("=" * 60)
        print(df.to_string(index=False))

        # 保存数据
        csv_file = 'N05_companies_with_sprite.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到 {csv_file}")

        # 可选：保存为Excel
        try:
            excel_file = 'N05_companies_with_sprite.xlsx'
            df.to_excel(excel_file, index=False)
            print(f"数据已保存到 {excel_file}")
        except:
            print("保存Excel需要安装openpyxl: pip install openpyxl")

        # 打印统计信息
        print("\n" + "=" * 60)
        print("统计信息:")
        print(f"总企业数: {len(df)}")
        print(f"估值总和: {pd.to_numeric(df['企业估值(亿元)'], errors='coerce').sum():.0f} 亿元")
        print(f"平均估值: {pd.to_numeric(df['企业估值(亿元)'], errors='coerce').mean():.0f} 亿元")

    else:
        print("提取失败")


if __name__ == "__main__":
    main()


"""
┌─────────────────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ 0   │ │ 1   │ │ 2   │ │ 3   │   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ 4   │ │ 5   │ │ 6   │ │ 7   │   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ 8   │ │ 9   │ │     │ │     │   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
└─────────────────────────────────────┘
        一张大图（雪碧图）
        
/* 只显示第3个数字（索引2） */
.sprite-number {
    width: 10px;           /* 显示区域宽度 */
    height: 12px;          /* 显示区域高度 */
    background-image: url('sprite.png');
    background-position: -20px 0px;  /* 向左偏移20px，显示第3个数字 */
    display: inline-block;
}


图片坐标系（左上角为原点）
(0,0) ──────────────────→ X轴（宽度）
  │
  │  ┌────────────────┐
  │  │                │
  │  │  裁剪区域       │
  │  │  left, top ───┐│
  │  │              ││
  │  │              ││
  │  └──────────────┘│
  │           right, bottom
  ↓
Y轴（高度）
"""
# ##
"""
1.
# 假设雪碧图包含数字 0-9，每个数字10x12像素
# 图片总宽度 = 10 * 10 = 100像素
# 图片总高度 = 12像素（单行排列） 一条 3 1 2 5 4 6 9 0 7 8 
sprite_img = Image.open('sprite.png')
print(f"雪碧图尺寸: {sprite_img.size}")  # (100, 12)

X坐标:  0    10   20   30   40   50   60   70   80   90   100
Y=0    ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
       │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │
Y=12   └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
       └─────────────────────────────────────────────────┘

2.
# 从CSS中提取的映射
css_mapping = {
    'abcdef': (-90, 0),   # 第10个数字（索引9）
    'cdefgh': (-21, 0),   # 第3个数字（索引2）
    'efghij': (-70, 0),   # 第8个数字（索引7）
    # ... 更多映射
}
# 左顶点，右下顶点 确定图像位置（其实，一个顶点加宽高便确定位置了）
# 数字0（位置 -0px）
box = (0, 0, 10, 12)     # 显示第1个数字

# 数字1（位置 -10px）
box = (10, 0, 20, 12)    # 显示第2个数字

# 数字2（位置 -20px）
box = (20, 0, 30, 12)    # 显示第3个数字

# 数字9（位置 -90px）
box = (90, 0, 100, 12)   # 显示第10个数字
平移 ============ 平移

裁剪框 = (abs(background-position-x), 
         abs(background-position-y), 
         abs(background-position-x) + 数字宽度,
         abs(background-position-y) + 数字高度)


雪碧图	                    一张包含多个小图片的大图
background-position        	CSS属性，负数表示向左/上移动
裁剪坐标	                    left = abs(x), top = abs(y)
裁剪尺寸	                    right = left + width, bottom = top + height
PIL裁剪	                    img.crop((left, top, right, bottom))
"""