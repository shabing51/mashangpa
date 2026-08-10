import ddddocr
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

""" 关键点是获得  cookie {'admin': '69b9f4da7f261e0fb94e95b250b3522f'} 只需要带着这个就能访问数据 
    而要获得 admin这个cookie, 必须   `正确识别验证码` 
    可以直接登录拿到 admin (admin 5分钟内有效)
    AI 说 : 响应 Cookie 由服务器生成，客户端只能接收和使用  不能模拟  但我看 admin 有点像md5签名 就是不知道对啥进行签名以及有没有`魔改` 
"""
base_url = 'https://spiderbuf.cn'

# 创建 Session 并设置通用 headers
session = requests.Session()
session.headers.clear()
session.headers.update({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
})
session.cookies.clear() # 多余的，本来就是 <RequestsCookieJar[]> 空的
# cookies = {
#     "_ga": "GA1.1.261017283.1775044945",
#     "_ga_7B42BKG1QE": "GS2.1.s1775094572$o2$g1$t1775101483$j60$l0$h0"
# }
# session.cookies.update(cookies)  # 不要带 cookies ############

def get_captcha_info(session):
    """获取验证码信息（使用同一个 session）"""
    url = "https://spiderbuf.cn/web-scraping-practice/web-scraping-with-captcha"
    response = session.get(url)

    soup = BeautifulSoup(response.text, "lxml")
    img = soup.find("img", attrs={"id": "image"})

    if img:
        # 实例化 ocr
        ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
        src = img.get("src")
        captchaId = src.split("/")[-1].replace(".png", "")
        img_url = base_url + src

        # 使用同一个 session 获取验证码图片
        img_response = session.get(img_url)
        result = ocr.classification(img_response.content)
        print("未进行登录时的session.cookies: ", session.cookies)
        print(f"验证码ID: {captchaId}")
        print(f"识别结果: {result}")

        return {
            "username": "admin",
            "password": "123456",
            "captchaSolution": result,
            "captchaId": captchaId
        }
    return None


def login(session):
    """登录并获取 Cookie"""
    # 先访问登录页面获取验证码
    print("正在获取验证码...")
    form_data = get_captcha_info(session)

    if not form_data:
        print("获取验证码失败")
        return False

    # 提交登录请求
    login_url = "https://spiderbuf.cn/web-scraping-practice/web-scraping-with-captcha/login"

    print(f"\n提交登录数据: {form_data}")
    response = session.post(login_url, data=form_data)

    # 调试信息
    # print(f"\n响应头: {response.headers}")
    print(f"Session 中的 Cookies: {session.cookies.get_dict()}")
    if not session.cookies:
        print("验证码识别错误(验证码是六位数字)")



def get_data(session):
    """获取需要登录才能访问的数据"""
    login(session)
    url = "https://spiderbuf.cn/web-scraping-practice/web-scraping-with-captcha/list"
    response = session.get(url)
    # print(response.text)
    print(f"\n数据页面状态码: {response.status_code}") # 永远都是 200 但不一定有数据
    html_io = StringIO(response.text)
    try:
        table = pd.read_html(html_io)[0]
        return table
    except Exception as e:
        print(e)


table_df = get_data(session)
try:
    print(table_df.to_string(index=False))
except Exception as e:
    print(e)