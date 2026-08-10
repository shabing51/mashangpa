import asyncio
from playwright.async_api import async_playwright

USER_AGENT = "yuanrenxue"

async def get_token(page, timestamp, page_num):
    token = await page.evaluate(
        """
        ({timestamp, page_num})=>{
            return window.md5(
                `/api/question/23${timestamp}${page_num}`
            );
        }
        """,
        {
            'timestamp': timestamp,
            'page_num': page_num
        }
    )
    return token

async def fetch_page(page, page_num):
    # 当前时间戳
    ts = await page.evaluate(
        """
        async (url)=>{
            let response = await fetch(
                url,
                {
                    headers:{
                        "Referer": "https://match.yuanrenxue.cn/match/23"
                    }
                }
            );
            return await response.text();
        }
        """,
        "https://match.yuanrenxue.cn/api/getTime"
    )

    # 生成token
    token = await get_token(page,ts,page_num)
    print(token)
    url = (
      "https://match.yuanrenxue.cn"
      f"/api/question/23?page={page_num}&pageSize=10&kw="
      f"&token={token}&now={ts}"
    )

    # 浏览器环境fetch
    data = await page.evaluate(
        """
        async (url)=>{
            let response = await fetch(url, {
                    headers:{
                        "Referer": "https://match.yuanrenxue.cn/match/23",
                    }
                });
            return await response.json();
        }
        """,
        url
    )
    return data


async def main():
    total = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={
                "width":1920,
                "height":1080
            },
             locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        # 添加cookie
        await context.add_cookies(
            [
                {
                    "name":"sessionid",
                    "value":"qcngxf1p24fbthxucr94o1std0qhdms8",
                    "domain":"match.yuanrenxue.cn",
                    "path":"/"
                }
            ]
        )
        page = await context.new_page()

        await page.add_init_script(
            """
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get:()=>undefined
                }
            )
            """
        )
        # 加载页面，让JS环境存在
        await page.goto(
            "https://match.yuanrenxue.cn/match/23",
            wait_until="networkidle"
        )
        # 确认md5函数存在
        check = await page.evaluate(
            """
            ()=>typeof window.md5
            """
        )
        print("md5:",check)

        # 循环请求几页
        for page_num in range(1,6):
            data = await fetch_page(page,page_num)
            print(data)
            print(page_num,data.get("data"))
            total += sum(data.get('data'))
        await browser.close()
    print(total)
    return total


if __name__ == "__main__":
    total = asyncio.run(main())