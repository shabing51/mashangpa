import os
import asyncio
import aiohttp
import aiofiles
import requests
from bs4 import BeautifulSoup

# 先获得一堆图片 urls 再请求下载即可
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices?order=rating",
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
    "_ga_7B42BKG1QE": "GS2.1.s1775044945$o1$g1$t1775048028$j43$l0$h0"
}
url = "https://spiderbuf.cn/web-scraping-practice/scraping-images-from-web"
response = requests.get(url, headers=headers, cookies=cookies)

soup = BeautifulSoup(response.text, "lxml")
# print(soup.prettify())  # 将 HTML/XML 文档格式化成美观、易读的格式（添加缩进和换行）
# 拿到所有 图片标签 拿到图片url
imgs = soup.find_all("img")
urls, base_url = [], 'https://spiderbuf.cn'
for img in imgs: # 拼接所有 url路径
    # print(img.get("src")) # /static/images/beginner/1ky9g5dp.jpg
    urls.append(base_url+img.get("src"))
# print(urls)

# 下载一张图片
async def download_img(url, session):
       res =  await session.get(url)
       async with aiofiles.open(f"./S05_images/{url.split('/')[-1]}", "wb") as f:
           await f.write(await res.content.read())  # 一定要 .read()

# 下载所有图片
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url_l in urls:
            tasks.append(download_img(url_l, session))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 创建保存图片的文件夹
    if not os.path.exists("../S05_images/"):
        os.makedirs("../S05_images/")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    # asyncio.run(main())