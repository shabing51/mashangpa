# 法一
# 一个个请求点开看，发现要爬的数据在 "https://spiderbuf.cn/web-scraping-practice/selenium-fingerprint-anti-scraper/api/MTc3NTE5NjkwMyw4MmZkODM1NWE4YmYyMThiNDIyMmYxZGE2M2YwZTRlNg=="
# 这个里面 CTRL+shift+F 搜索 selenium-fingerprint-anti-scraper/api 点进去就看见请求路径(MTc3NTE5NjkwMyw4MmZkODM1NWE4YmYyMThiNDIyMmYxZGE2M2YwZTRlNg==)是如何生成的了 之后发请求就行了\
# 往上看发现检测 if ((!navigator.webdriver) & (navigator.plugins.length > 0) & (user_agent.indexOf('headless') < 0))这是针对selenium的
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
# # 伪造 plugins（添加假插件）
# driver.execute_script("""
#     Object.defineProperty(navigator, 'plugins', {
#         get: () => {
#             return {
#                 length: 5,
#                 item: (index) => {
#                     return {
#                         name: ['Chrome PDF Plugin', 'Chrome PDF Viewer', 'Native Client'][index] || null,
#                         filename: ['internal-pdf-viewer', 'mhjfbmdgcfjbbpaeojofohoefgiehjai', 'internal-nacl-plugin'][index] || null
#                     };
#                 }
#             };
#         }
#     });
# """)
#
# # 可选：修改其他可能的检测点
# driver.execute_script("""
#     // 修改 languages
#     Object.defineProperty(navigator, 'languages', {
#         get: () => ['zh-CN', 'zh', 'en']
#     });
#
#     // 修改 platform
#     Object.defineProperty(navigator, 'platform', {
#         get: () => 'Win32'
#     });
# """)



# 查询参数生成关键操作:
# var timeStamp = Math.trunc(new Date().getTime() / 1000);
#     var _md5 = md5(timeStamp);
#     var s = btoa(`${timeStamp},${_md5}`);
""" 检测JS代码
var user_agent = navigator.userAgent;
if ((!navigator.webdriver) & (navigator.plugins.length > 0) & (user_agent.indexOf('headless') < 0)) {
    console.log(navigator.webdriver);
    console.log(navigator.plugins.length);
    console.log(user_agent.indexOf('headless'));
    var timeStamp = Math.trunc(new Date().getTime() / 1000);
    var _md5 = md5(timeStamp);
    var s = btoa(`${timeStamp},${_md5}`);

    fetch("/web-scraping-practice/selenium-fingerprint-anti-scraper/api/" + s).then(function (response) {
        return response.json();
    }).then(function (data) {
        var dataContent = document.querySelector('#dataContent > tbody');
        data.forEach((value, index) => {
            var row = dataContent.insertRow();
            var rankingCell = row.insertCell();
            rankingCell.innerText = value.ranking;

            var passwdCell = row.insertCell();
            passwdCell.innerText = value.passwd;

            var time_to_crackItCell = row.insertCell();
            time_to_crackItCell.innerText = value.time_to_crack_it;

            var used_countCell = row.insertCell();
            used_countCell.innerText = value.used_count;
        })
    });
}
"""

"""
import time
import base64
import hashlib
from curl_cffi import requests

def get_param():
    timestamp =int(time.time() * 1)
    _md5 = hashlib.md5(str(timestamp).encode('utf-8')).hexdigest()
    s_tmp = f"{timestamp},{_md5}"
    s = base64.b64encode(s_tmp.encode('utf-8')).decode('utf-8')
    return s

base_url = "https://spiderbuf.cn/web-scraping-practice/selenium-fingerprint-anti-scraper/api/"

url = f"{base_url}{get_param()}"

# 发请求， 拿数据
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(resp.json())

"""

# 法二,使用selenium 过检测拿数据

import pandas as pd
from io import StringIO  # 前面两个库用于快速从HTML中提取表格数据
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_chrome_driver(
    headless=False,
    stealth_mode=True,
    download_path=None,
    proxy=None,
    user_agent=None,
    window_size=(1920, 1080),
    exec_path = None
):
    """
    创建配置好的Chrome驱动

    Args:
        headless: 是否无头模式
        stealth_mode: 是否启用反检测
        download_path: 下载路径
        proxy: 代理地址
        user_agent: 用户代理
        window_size: 窗口大小
        exec_path: 驱动路径
    """
    if exec_path:
        service = Service(executable_path= exec_path)
    else:
        service = Service(executable_path= r"C:\webdriver\chromedriver.exe")
    chrome_options = Options()

    # 1. 基础配置
    chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    # chrome_options.add_argument("--start-maximized") # 最大化
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')

    # 2. 性能优化
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')

    # 3. 安全相关
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-web-security')

    # 4. 无头模式
    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    # 5. 反检测模式
    if stealth_mode:
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # 加载指纹伪装插件
        # chrome_options.add_extension('fingerprint-spoofing-extension.crx')

    # 6. 下载配置
    if download_path:
        prefs = {
            'download.default_directory': download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        chrome_options.add_experimental_option('prefs', prefs)

    # 7. 代理配置
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    # 8. User-Agent配置
    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')
    elif stealth_mode:
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # 9. 其他配置
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--lang=zh-CN')

    # 创建驱动
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 10. 额外的反检测脚本（stealth模式）
    if stealth_mode:
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                delete navigator.webdriver;
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
            '''
        })

    return driver

# 生成 driver
driver = create_chrome_driver(
    headless=False,
    stealth_mode=True,
    download_path=r'D:\Downloads',
    window_size=(1920, 1080),
    exec_path=None
)
driver.maximize_window()
driver.implicitly_wait(10) # 全局隐式等待
driver.get("https://spiderbuf.cn/web-scraping-practice/selenium-fingerprint-anti-scraper")

wait = WebDriverWait(driver, 10) # 显示等待针对某个元素节点

wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='dataContent']/tbody/tr[1]/td[1]")))
# 拿到js执行过后浏览器渲染过后的源代码（Element,元素）
html = driver.page_source
# 从包含目标数据的HTML中提取目标数据
html_io = StringIO(html)
table_df = pd.read_html(html_io)[0] # 不知道是不是列表

print(table_df)

driver.quit()