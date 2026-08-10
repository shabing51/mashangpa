import requests
from lxml import etree
import pandas as pd
import re

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775108645$o1$g1$t1775110155$j60$l0$h0"
}

url = "https://spiderbuf.cn/web-scraping-practice/random-css-classname"
html_bytes = requests.get(url, headers=headers, cookies=cookies).content
html = html_bytes.decode()
root = etree.HTML(html)

# 提取所有文本内容
divs = root.xpath('/html/body/main/div[2]/div')

# 清理和整理数据
questions = []
current_question = {}
question_pattern = re.compile(r'^(\d+)\.(.+)$')  # 匹配 "0.入门基础"

for div in divs:
    if div.text:
        text = div.text.replace("&nbsp", '').strip()
        if not text:  # 跳过空行
            continue

        # 检查是否是序号行（如 "0.入门基础"）
        match = question_pattern.match(text)
        if match:
            # 如果已有当前题目，先保存
            if current_question:
                questions.append(current_question)

            # 开始新题目
            current_question = {
                '序号': int(match.group(1)),
                '分类': match.group(2),
                '题目': ''
            }
        else:
            # 这是题目内容
            if current_question:
                if current_question['题目']:
                    current_question['题目'] += ' ' + text  # 拼接多行题目
                else:
                    current_question['题目'] = text

# 保存最后一个题目
if current_question:
    questions.append(current_question)

# 转换为DataFrame
df = pd.DataFrame(questions)

print(f"共提取 {len(df)} 道题目")
print("\n前10道题目预览:")
print(df.head(10))

# 保存到文件
df.to_csv('python_questions.csv', index=False, encoding='utf-8-sig')
print("\n数据已保存到 python_questions.csv")