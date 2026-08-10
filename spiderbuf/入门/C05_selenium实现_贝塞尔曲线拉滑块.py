import pandas as pd
from io import StringIO
import time, random, numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def ease_out_quart(x):
    """缓动函数：先快后慢"""
    return 1 - pow(1 - x, 4)
"""
# 假设总拖动距离是 215 像素
total_distance = 215
# 当拖动到 25% 时
x = 0.25
result = ease_out_quart(0.25)  # 返回约 0.68
# 实际完成距离 = 215 * 0.68 = 146 像素
# 这意味着：只用了 25% 的时间，就完成了 68% 的距离（先快）

def ease_in_quart(x):
    # 先慢后快（点击按钮）
    return x ** 4

def ease_in_out_quart(x):
   # 先慢→快→慢（标准动画）
    return 2 * x ** 2 if x < 0.5 else 1 - (-2 * x + 2) ** 2 / 2

def ease_out_bounce(x):
   
    # 缓动函数：先快后慢，结束时带弹跳效果
    # x: 0 到 1 之间的进度
    # 返回: 0 到 1 之间的完成比例
   
    if x < 1 / 2.75:
        return 7.5625 * x * x
    elif x < 2 / 2.75:
        x -= 1.5 / 2.75
        return 7.5625 * x * x + 0.75
    elif x < 2.5 / 2.75:
        x -= 2.25 / 2.75
        return 7.5625 * x * x + 0.9375
    else:
        x -= 2.625 / 2.75
        return 7.5625 * x * x + 0.984375
"""

def get_bezier_tracks(distance, duration=0.8):
    """
    使用缓动函数生成贝塞尔曲线轨迹

    # 假设 distance=215, duration=0.8

    # 第1次循环 (t=0.0):
    progress = t / duration = 0.0 / 0.8 = 0.0      # 进度 0%
    ratio = ease_out_quart(0.0) = 0.0              # 完成比例 0%
    offset = round(0.0 * 215) = 0                  # 累计移动 0px

    # 第2次循环 (t=0.05):
    progress = 0.05 / 0.8 = 0.0625                 # 进度 6.25%
    ratio = ease_out_quart(0.0625) ≈ 0.23          # 完成比例 23%
    offset = round(0.23 * 215) = 49                # 累计移动 49px

    # 第3次循环 (t=0.10):
    progress = 0.10 / 0.8 = 0.125                  # 进度 12.5%
    ratio = ease_out_quart(0.125) ≈ 0.41           # 完成比例 41%
    offset = round(0.41 * 215) = 88                # 累计移动 88px

    # 第4次循环 (t=0.15):
    progress = 0.15 / 0.8 = 0.1875                 # 进度 18.75%
    ratio = ease_out_quart(0.1875) ≈ 0.57          # 完成比例 57%
    offset = round(0.57 * 215) = 123               # 累计移动 123px
    # ... 继续到 t=0.80

    track = offset - offsets[-1]  # 当前累计 - 上次累计 = 本次移动距离
    t=0.65s: progress=0.81, ratio=0.999, offset=215, track=1
    1 - (1-0.65/0.8)**4 = 0.998764038  ==>215 * 0.998764038 = 214.734268...
    """
    tracks = []
    offsets = [0]

    for t in np.arange(0.0, duration, 0.05): # 每0.05秒生成一个点
        offset = round(ease_out_quart(t / duration) * distance) # 当前总偏移
        track = offset - offsets[-1] # 本次移动距离
        tracks.append(track)
        offsets.append(offset)

    return tracks[1:]  # 去除第一个0


def drag_with_bezier(driver, slider, distance):
    """使用贝塞尔曲线轨迹拖动"""
    action = ActionChains(driver)
    action.click_and_hold(slider).perform() # 按住滑块

    tracks = get_bezier_tracks(distance)  # 获取轨迹点
    # print(tracks) # [49, 40, 32, 26, 20, 15, 11, 9, 5, 4, 2, 1, 1, 0, 0]
    for track in tracks:
        action.move_by_offset(track, random.randint(-1, 1)).perform() # 移动
        time.sleep(random.uniform(0.01, 0.03)) # 随机停顿 真实模拟用户拉滑块

    action.release().perform()  # 释放滑块

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

driver.get("https://spiderbuf.cn/web-scraping-practice/scraper-practice-c05")

wait = WebDriverWait(driver, 10)
# driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#slider")))
slider = driver.find_element(By.CSS_SELECTOR, "#slider")

drag_with_bezier(driver, slider, 215)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='flightTable']/tbody/tr[20]/td[3]")))

html = driver.page_source
html_io = StringIO(html)
df_table = pd.read_html(html_io)[0]
print(df_table.to_string(index=False))

driver.quit()
