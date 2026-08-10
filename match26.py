import asyncio
from playwright.async_api import async_playwright

USER_AGENT = "yuanrenxue"

async def get_token(page, now, page_num):
    token = await page.evaluate(
        """
        async ({now, page_num})=>{
            return window.x(`/api/question/26${now}${page_num}`);
        }
        """,
        {
            "now": now,
            "page_num": page_num
        }
    )
    return token



async def fetch_page(page, page_num):
    now = await page.evaluate(
        """
        async (url)=>{
            let response = await fetch(
                url,
                {
                    headers:{
                        "Referer":"https://match.yuanrenxue.cn/match/26"
                    }
                }
            )
            return await response.text()
        }
        """,
        "https://match.yuanrenxue.cn/api/getTime"
    )

    token = await get_token(page, now, page_num)

    url = (
        "https://match.yuanrenxue.cn"
        f"/api/question/26?page={page_num}&pageSize=10&kw="
        f"&token={token}&now={now}"
    )
    data = await page.evaluate(
        """
        async (url)=>{
            let response = await fetch(
                url,
                {
                    headers:{
                        "Referer":"https://match.yuanrenxue.cn/match/26"
                    }
                }
            )

            let data = await response.json();
            console.log(data);
            return data;
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
        # add_cookies
        await context.add_cookies([
            {
                "name":"sessionid",
                "value":"1i5v0k8r6a43wlsyiawqngaitay2n0xi",
                "domain":"match.yuanrenxue.cn",
                "path":"/"
            }
        ])

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
            "https://match.yuanrenxue.cn/match/26",
            wait_until="networkidle"
        )

        check = await page.evaluate(
            """
            ()=>typeof window.x
            """
        )
        print("window.x: ", check)

        try:
            for page_num in range(1,6):
                data = await fetch_page(page, page_num)
                print(data)
                print(f"第{page_num}页数据: {data['data']}")
                total += sum(data["data"])
        except Exception as e:
            print(f"something wrong, try again.{e}")
        finally:
            await browser.close()

        print(total)
        return total

if __name__ == "__main__":
    asyncio.run(main())