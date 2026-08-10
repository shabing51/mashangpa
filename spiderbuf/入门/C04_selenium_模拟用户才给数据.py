import re
import math
import time
import random
import pandas as pd
from lxml import etree
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def smart_click(driver, element, safe_mode=True):
    """智能点击：根据场景选择方法"""
    if safe_mode:  # 元素不可交互（disabled、隐藏） 报错 ElementNotInteractableException
        # 反爬场景：完整模拟  元素不在视口内报错 MoveTargetOutOfBoundsException
        ActionChains(driver).move_to_element(element).pause(0.2).click().perform()
    else:
        # 速度优先：直接点击
        element.click()

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


def bezier_3rd_order(p0: Tuple[float, float],
                     p1: Tuple[float, float],
                     p2: Tuple[float, float],
                     p3: Tuple[float, float],
                     t: float) -> Tuple[float, float]:
    """
    计算三阶贝塞尔曲线上的点
    B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
    """
    x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
    y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
    return (x, y)

def generate_bezier_points(start: Tuple[float, float],
                           end: Tuple[float, float],
                           control_points: List[Tuple[float, float]] = None,
                           num_points: int = 50) -> List[Tuple[float, float]]:
    """
    生成贝塞尔曲线上的点集
    :param start: 起点坐标
    :param end: 终点坐标
    :param control_points: 控制点列表（1-3个，自动补全）
    :param num_points: 生成点的数量
    """
    if control_points is None:
        # 自动生成随机控制点，制造自然弧度
        control_points = generate_natural_control_points(start, end)

    points = []
    for i in range(num_points):
        t = i / (num_points - 1)  # 0到1均匀分布

        if len(control_points) == 1:
            # 二阶贝塞尔
            p0, p1, p2 = start, control_points[0], end
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            points.append((x, y))

        elif len(control_points) == 2:
            # 三阶贝塞尔（最常用）
            p0, p1, p2, p3 = start, control_points[0], control_points[1], end
            points.append(bezier_3rd_order(p0, p1, p2, p3, t))

        elif len(control_points) >= 3:
            # 四阶以上（简化处理，只用前三个）
            points.append(bezier_3rd_order(start, control_points[0], control_points[1], end, t))

    return points

def generate_mouse_trajectory(driver, container_id, duration=2):
    """生成真实的鼠标轨迹"""
    container = driver.find_element(By.ID, container_id)
    action = ActionChains(driver)

    location = container.location
    size = container.size

    start_x = location['x'] + size['width'] // 2
    start_y = location['y'] + size['height'] // 2

    points = [(start_x, start_y)]
    for _ in range(random.randint(18, 36)):
        x = start_x + random.randint(-100, 100)
        y = start_y + random.randint(-70, 80)
        points.append((x, y))

    for x, y in points:
        try:
            action.move_to_element(container).move_by_offset(
                x - location['x'] - size['width'] // 2,
                y - location['y'] - size['height'] // 2
            ).perform()
            time.sleep(random.uniform(0.005, 0.02))
        except:
            pass

    return len(points)

# 注: 用贝塞尔曲线效果更加类人
def generate_natural_control_points(start: Tuple[float, float],
                                    end: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    生成自然的控制点（模拟人类手部运动）
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # 随机决定曲线类型
    curve_type = random.choice(['slight_arc', 'overshoot', 's_shape', 'random'])

    if curve_type == 'slight_arc':
        # 轻微弧度（最常见）
        offset_x = random.uniform(-distance * 0.1, distance * 0.1)
        offset_y = random.uniform(-distance * 0.2, distance * 0.1)
        p1 = (start[0] + dx * 0.33 + offset_x, start[1] + dy * 0.33 + offset_y)
        p2 = (start[0] + dx * 0.66 + offset_x, start[1] + dy * 0.66 + offset_y)

    elif curve_type == 'overshoot':
        # 过冲（超出目标再回来）
        overshoot = distance * random.uniform(0.05, 0.15)
        p1 = (start[0] + dx * 0.4, start[1] + dy * 0.4 - overshoot)
        p2 = (start[0] + dx * 0.7, start[1] + dy * 0.7 + overshoot)

    elif curve_type == 's_shape':
        # S形曲线
        p1 = (start[0] + dx * 0.3, start[1] + dy * 0.2 - distance * 0.1)
        p2 = (start[0] + dx * 0.7, start[1] + dy * 0.8 + distance * 0.1)

    else:
        # 完全随机
        p1 = (start[0] + dx * random.uniform(0.2, 0.5),
              start[1] + dy * random.uniform(0.2, 0.5) + random.uniform(-distance * 0.2, distance * 0.2))
        p2 = (start[0] + dx * random.uniform(0.5, 0.8),
              start[1] + dy * random.uniform(0.5, 0.8) + random.uniform(-distance * 0.2, distance * 0.2))

    return [p1, p2]
def generate_timing_points(num_points: int,
                           speed_variation: float = 0.3) -> List[float]:
    """
    生成带有速度变化的t值序列（模拟人类移动：慢-快-慢）
    :param num_points: 点数
    :param speed_variation: 速度变化程度（0-1）
    """
    t_values = []
    for i in range(num_points):
        # 使用正弦曲线模拟加速-匀速-减速
        raw_t = i / (num_points - 1)
        # 易缓-易缓曲线（ease-in-out）
        eased_t = 0.5 * (1 - math.cos(math.pi * raw_t))

        # 添加随机扰动
        noise = random.uniform(-speed_variation, speed_variation) * raw_t * (1 - raw_t)
        final_t = max(0, min(1, eased_t + noise))
        t_values.append(final_t)

    return t_values
def generate_smooth_trajectory(start: Tuple[float, float],
                               end: Tuple[float, float],
                               num_points: int = 60) -> List[Tuple[float, float]]:
    """
    生成平滑的鼠标轨迹（带速度变化）
    """
    # 生成控制点
    control_points = generate_natural_control_points(start, end)

    # 生成曲线点
    bezier_points = generate_bezier_points(start, end, control_points, num_points)

    # 生成速度变化的时间分布
    t_values = generate_timing_points(num_points, speed_variation=0.3)

    # 根据速度变化重新采样
    final_points = []
    for t in t_values:
        idx = int(t * (len(bezier_points) - 1))
        final_points.append(bezier_points[idx])

    return final_points
def bezier_mouse_trajectory(driver, container_id, duration=2):
    """
    针对400×120容器的贝塞尔曲线轨迹
    """
    container = driver.find_element(By.ID, container_id)
    location = container.location
    size = container.size

    # 目标点：容器中心
    target_x = location['x'] + size['width'] // 2
    target_y = location['y'] + size['height'] // 2

    # 起点：从容器外某个随机位置开始
    start_x = location['x'] + random.randint(-150, -50)
    start_y = location['y'] + random.randint(-100, size['height'] + 100)

    # 生成贝塞尔曲线轨迹
    trajectory = generate_smooth_trajectory(
        (start_x, start_y),
        (target_x, target_y),
        num_points=random.randint(20, 36)
    )

    # 执行移动
    action = ActionChains(driver)
    step_delay = duration / len(trajectory)

    for x, y in trajectory:
        # 移动到元素
        action.move_to_element(container).move_by_offset(
            x - location['x'] - size['width'] // 2,
            y - location['y'] - size['height'] // 2
        ).perform()
        time.sleep(random.uniform(step_delay * 0.7, step_delay * 1.3))

    return len(trajectory)


def human_like_click(driver, element):
    """模拟人类点击"""
    action = ActionChains(driver)
    action.move_to_element(element).perform()
    time.sleep(random.uniform(0.3, 0.6))

    for _ in range(random.randint(3, 6)):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-1, 1)
        action.move_by_offset(offset_x, offset_y).perform()
        time.sleep(random.uniform(0.05, 0.1))

    element.click()


# 实例化 driver
driver = create_chrome_driver(
    headless=False,
    stealth_mode=True,
    download_path=r'D:\Downloads',
    window_size=(1920, 1080),
    exec_path=None
)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://spiderbuf.cn/web-scraping-practice/scraper-practice-c04")

wait = WebDriverWait(driver, 10)
# 过检测,模拟用户操作
try:
    # 1. 等待验证码容器出现
    captcha_container = wait.until(EC.presence_of_element_located((By.ID, "captcha_container")))
    print("✓ 验证码容器已加载")

    # 2. 生成鼠标轨迹
    print("正在生成鼠标轨迹...")
    # trajectory_points = generate_mouse_trajectory(driver, "captcha_container", duration=2)
    trajectory_points = bezier_mouse_trajectory(driver, "captcha_container") # bezier曲线点
    print(f"✓ 已生成 {trajectory_points} 个轨迹点")

    # 3. 等待复选框出现
    checkbox = wait.until(EC.element_to_be_clickable((By.ID, "captcha")))
    print("✓ 复选框已出现")

    # 4. 模拟人类点击
    human_like_click(driver, checkbox)
    print("✓ 复选框已点击")

    # 5. 等待帖子加载
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#posts > div")))
    print("✓ 帖子已加载")

    time.sleep(1)

except Exception as e:
    print(f"验证过程出错: {e}")
# driver.get_window_position() ########################
# # 获取当前鼠标位置（通过JS）
# current_pos = driver.execute_script("""
#     return {x: window.mouseX || 0, y: window.mouseY || 0};
# """)
# 获取页面源码
html = driver.page_source
driver.quit()

# ========== 使用 lxml 解析，正确处理评论数的多个 digit ==========
root = etree.HTML(html)

# 选择所有帖子 posts->post
posts = root.xpath("//div[@id='posts']/div")
print(f"找到 {len(posts)} 个帖子")

all_data = []
# 解析数据
for i, post in enumerate(posts):
    try:
        # 提取标题
        title_elements = post.xpath(".//h3/text()")
        title = title_elements[0].strip() if title_elements else ""

        # 提取内容
        content_elements = post.xpath(".//p/text()")
        content = content_elements[0].strip() if content_elements else ""

        # 提取阅读数 - 直接提取 span 中的文本
        read_span = post.xpath(".//span[contains(text(), '阅读数')]/text()")
        if read_span:
            read_text = read_span[0].strip()
            reads = int(re.search(r'\d+', read_text).group())
        else:
            reads = 0

        # 提取点赞数
        like_span = post.xpath(".//span[contains(text(), '点赞数')]/text()")
        if like_span:
            like_text = like_span[0].strip()
            likes = int(re.search(r'\d+', like_text).group())
        else:
            likes = 0

        # 提取转发数
        share_span = post.xpath(".//span[contains(text(), '转发数')]/text()")
        if share_span:
            share_text = share_span[0].strip()
            shares = int(re.search(r'\d+', share_text).group())
        else:
            shares = 0

        # 提取评论数 - 需要合并多个 digit span
        # 方法1：获取所有 digit span 的文本并拼接
        digit_spans = post.xpath(".//span[@class='comments']//span[@class='digit']/text()")
        if digit_spans:
            comments = int("".join(digit_spans))
        else:
            # 方法2：如果没有 digit span，尝试直接提取
            comment_span = post.xpath(".//span[contains(text(), '评论数')]/text()")
            if comment_span:
                comment_text = comment_span[0].strip()
                comments = int(re.search(r'\d+', comment_text).group())
            else:
                comments = 0

        data = {
            "title": title,
            "content": content,
            "reads": reads,
            "likes": likes,
            "shares": shares,
            "comments": comments,
        }
        all_data.append(data)
        print(f"✓ 解析成功: {title[:30]}... (阅读数: {reads}, 评论数: {comments})")

    except Exception as e:
        print(f"解析帖子 {i + 1} 出错: {e}")
        continue

print(f"\n成功解析 {len(all_data)} 个帖子")

# 创建 DataFrame
if all_data:
    df = pd.DataFrame(all_data)

    # 计算阅读量与评论量之和
    df["reads_plus_comments"] = df["reads"] + df["comments"]
    mean_v, std_v, sum_ = df["reads_plus_comments"].agg(['mean', 'std', 'sum'])

    print("\n" + "=-=" * 60)
    print(df.to_string(index=False))
    print("=-=" * 60)
    print(f"\n统计结果:")
    print(f"  阅读量与评论量之和的均值: {mean_v:.2f}")
    print(f"  标准差: {std_v:.2f}")
    print(f"  总和: {sum_}")

    # 保存到 CSV
    df.to_csv("weibo_data.csv", index=False, encoding="utf-8-sig")
    print("\n数据已保存到 weibo_data.csv")
else:
    print("没有解析到任何数据")

"""
✓ 验证码容器已加载
正在生成鼠标轨迹...
✓ 已生成 30 个轨迹点
✓ 复选框已出现
✓ 复选框已点击
✓ 帖子已加载
找到 10 个帖子
✓ 解析成功: Python 爬虫入门指南... (阅读数: 1500, 评论数: 50)
✓ 解析成功: 使用 BeautifulSoup 解析网页... (阅读数: 1200, 评论数: 45)
✓ 解析成功: Scrapy 框架实战教程... (阅读数: 1300, 评论数: 60)
✓ 解析成功: 爬虫与反爬虫技术... (阅读数: 1100, 评论数: 40)
✓ 解析成功: 动态网页抓取：Selenium 与 Puppeteer... (阅读数: 1400, 评论数: 65)
✓ 解析成功: 爬虫数据存储与清洗... (阅读数: 1000, 评论数: 35)
✓ 解析成功: 爬虫与 SEO 数据分析... (阅读数: 1600, 评论数: 70)
✓ 解析成功: 爬虫性能优化技巧... (阅读数: 900, 评论数: 30)
✓ 解析成功: 爬虫与 API 数据抓取... (阅读数: 950, 评论数: 32)
✓ 解析成功: 爬虫项目实战：SEO 工具开发... (阅读数: 1700, 评论数: 75)

成功解析 10 个帖子

====================================================================================================
                      title                                content  reads  likes  shares  comments  reads_plus_comments
              Python 爬虫入门指南          学习如何使用 Python 编写简单的爬虫，抓取网页数据。   1500    200      90        50                 1550
      使用 BeautifulSoup 解析网页 掌握 BeautifulSoup 库，轻松解析 HTML 和 XML 数据。   1200    180      80        45                 1245
              Scrapy 框架实战教程       通过 Scrapy 框架快速构建高效爬虫，适用于大规模数据抓取。   1300    220     100        60                 1360
                   爬虫与反爬虫技术                  了解常见的反爬虫机制，并学习如何绕过限制。   1100    150      70        40                 1140
动态网页抓取：Selenium 与 Puppeteer   使用 Selenium 和 Puppeteer 抓取动态渲染的网页内容。   1400    250     110        65                 1465
                  爬虫数据存储与清洗                将抓取的数据存储到数据库，并进行清洗和预处理。   1000    130      60        35                 1035
               爬虫与 SEO 数据分析            通过爬虫抓取 SEO 数据，分析关键词排名和流量趋势。   1600    280     120        70                 1670
                   爬虫性能优化技巧                     优化爬虫性能，提高抓取速度和稳定性。    900    110      50        30                  930
               爬虫与 API 数据抓取            学习如何通过 API 接口抓取数据，避免直接爬取网页。    950    120      55        32                  982
            爬虫项目实战：SEO 工具开发         开发一个 SEO 分析工具，结合爬虫技术抓取和分析网站数据。   1700    300     130        75                 1775
====================================================================================================

统计结果:
  阅读量与评论量之和的均值: 1315.20
  标准差: 296.35
  总和: 13152.0

数据已保存到 weibo_data.csv

"""

