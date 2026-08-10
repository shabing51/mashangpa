from lxml import etree
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
        driver.execute_script("""
            Object.getOwnPropertyNames(window).forEach(prop => {
                if (prop.startsWith('cdc_')) {
                    delete window[prop];
                }
            });
        """)
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

driver.get("https://spiderbuf.cn/web-scraping-practice/scraper-practice-c06")

wait = WebDriverWait(driver, 10)
driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")

wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn-page")))

ele = driver.find_element(By.CSS_SELECTOR, ".btn-page")
ele.click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="items"]/div[20]')))
page_source = driver.page_source
root = etree.HTML(page_source)
rating_list = list(map(float, root.xpath("//div[@class='detail']/p[1]/span[2]/text()")))
print(rating_list) #
rating_sum = sum(map(float, root.xpath("//div[@class='detail']/p[1]/span[2]/text()")))
print(rating_sum)
"""
[9.3, 9.3, 9.3, 9.2, 9.2, 9.2, 9.2, 9.2, 9.2, 9.2, 9.1, 9.1, 9.1, 9.1, 9.1, 9.0, 9.0, 9.0, 9.0, 9.0]
182.79999999999998
"""