import time
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def create_chrome_driver(
        headless=False,
        stealth_mode=True,
        download_path=None,
        proxy=None,
        user_agent=None,
        window_size=(1920, 1080),
        exec_path=None
):
    """创建配置好的Chrome驱动"""
    if exec_path:
        service = Service(executable_path=exec_path)
    else:
        service = Service(executable_path=r"C:\webdriver\chromedriver.exe")
    chrome_options = Options()

    chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-web-security')

    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    if stealth_mode:
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    if download_path:
        prefs = {
            'download.default_directory': download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        chrome_options.add_experimental_option('prefs', prefs)

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')
    elif stealth_mode:
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--lang=zh-CN')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    if stealth_mode:
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                delete navigator.webdriver;
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'driver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
                window.chrome = { runtime: {} };
            '''
        })

    return driver

# 实例化 driver
driver = create_chrome_driver(
    headless=False,
    stealth_mode=True,
    download_path=r'D:\Downloads',
    window_size=(1920, 1080),
    exec_path=None
)
driver.maximize_window()
driver.implicitly_wait(12)
driver.get("https://spiderbuf.cn/web-scraping-practice/web-scraping-practice-c13")

wait = WebDriverWait(driver, 12)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='items']/table/tbody/tr[20]/td[7]")))
html = driver.page_source
html_io = StringIO(html)
table = pd.read_html(html_io)[0]
print(table.to_string(index=False))
print(table['CPC'].agg("mean"))