import requests
import pandas as pd
from io import StringIO

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practice/web-pagination-scraper?pageno=2",
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
    "_ga": "GA1.1.261017283.1775044945",
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775049705$j22$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/web-pagination-scraper"


def get_page(page_no):
    """获取单页数据，返回 DataFrame"""
    params = {"pageno": page_no}
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return pd.DataFrame()

    # 解析 HTML
    html_io = StringIO(response.text)
    tables = pd.read_html(html_io)

    if tables:
        return tables[0]  # 返回第一个表格, 页面其实只有一个表格
    else:
        return pd.DataFrame()


def main():
    """获取所有页面数据"""
    all_data = []

    for page_no in range(1, 6):
        print(f"正在获取第 {page_no} 页...")
        df = get_page(page_no)
        if not df.empty:
            all_data.append(df)
        else:
            print(f"第 {page_no} 页没有数据")

    # 拼接所有 DataFrame
    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        return result
    else:
        return pd.DataFrame()


# 执行
df_result = main()

# print(df_result)
df_result.drop(columns =['序号', ], inplace=True)
print(df_result)
df_result.to_html(r"./S04_result.html", encoding="utf-8")  ##### df  to html
# 保存到 CSV
# df_result.to_csv('pagination_data.csv', index=False, encoding='utf-8-sig') # ❌ 使用 utf-8 保存，Excel 打开会乱码