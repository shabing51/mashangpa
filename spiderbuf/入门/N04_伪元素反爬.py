import re
from xml.etree.ElementPath import prepare_self

import requests
from bs4 import BeautifulSoup


# 特征:HTML 有大量空标签(内容少) CSS文件大量::before and ::after
"""
找到目标元素的所有class
<span class="mnopqr pkenmc">.

在CSS中查找这些class的规则
.mnopqr::before { content: "9"; }
.mnopqr::after { content: "1"; }
.pkenmc::after { content: "7"; }
按CSS层叠顺序应用（后定义的覆盖先定义的）
初始: [before] + 原始文本 + [after]
应用.mnopqr: ["9"] + "." + ["1"]  → "9.1"
应用.pkenmc: ["9"] + "." + ["7"]  → "9.7"
"""

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/4?order=rating",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775116100$o2$g1$t1775118577$j44$l0$h0"
}

# 获取页面
url = "https://spiderbuf.cn/web-scraping-practice/css-pseudo-elements"
response = requests.get(url, headers=headers, cookies=cookies)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

def get_css_mapping(soup):
    # 提取所有<style>标签中的CSS规则
    styles = soup.find_all('style')
    css_text = '\n'.join([style.string for style in styles if style.string])

    # 解析伪元素规则
    pseudo_rules = {}
    pattern = r'\.(\w+)::(before|after)\s*\{\s*content:\s*"([^"]+)"\s*;\s*\}'
    matches = re.findall(pattern, css_text)

    for class_name, pseudo_type, content in matches:
        key = f"{class_name}::{pseudo_type}"
        pseudo_rules[key] = content
    return pseudo_rules

pseudo_rules = get_css_mapping(soup)

print("提取的伪元素规则:")
for rule, content in pseudo_rules.items():
    print(f"{rule} -> '{content}'")


def crack_pseudo_element_antiscraping_v3(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取CSS映射
    mapping = {}
    for style in soup.find_all('style'):
        if style.string:
            pattern = r'\.(\w+)::(before|after)\s*\{\s*content:\s*"([^"]+)"\s*;\s*\}'
            for match in re.finditer(pattern, style.string):
                mapping[(match.group(1), match.group(2))] = match.group(3)
    # print(mapping)
    movies = []
    movie_blocks = soup.find_all('div', class_='col-xs-12 col-lg-12')

    for block in movie_blocks:
        h2 = block.find('h2')
        if not h2:
            continue

        # 直接找带有伪元素类的span
        # 这些类名通常是被CSS定义的
        rating_spans = []
        for span in block.find_all('span'):
            classes = span.get('class', [])
            # 检查这个span是否有对应的伪元素规则
            for cls in classes:
                if (cls, 'before') in mapping or (cls, 'after') in mapping:
                    rating_spans.append(span)
                    break
        # 构建评分
        rating_parts = []
        for span in rating_spans[:3]:  # 只取前3个
            classes = span.get('class', [])
            text = span.get_text(strip=True)

            for cls in classes:
                if (cls, 'before') in mapping:
                    rating_parts.append(mapping[(cls, 'before')])
            if text:
                rating_parts.append(text)
            for cls in classes[::-1]:
                if (cls, 'after') in mapping:
                    rating_parts.append(mapping[(cls, 'after')])
        raw_rating = ''.join(rating_parts)
        rating_match = re.search(r'(\d\.\d)', raw_rating)
        rating = rating_match.group(1) if rating_match else raw_rating

        movies.append({
            'title': h2.get_text(strip=True),
            'rating': rating
        })

    return movies

movies = crack_pseudo_element_antiscraping_v3(url)
for movie in movies:
    print(movie)

