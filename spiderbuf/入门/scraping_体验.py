from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher, AsyncFetcher

# fetch 方法会直接返回一个 Adaptor 对象，代表整个页面
page = StealthyFetcher.fetch('https://quotes.toscrape.com/')

# 检查是否获取成功
print(f"状态码: {page.status}") # 输出: 状态码: 200

# 1. 使用CSS选择器提取所有名言文本
quotes = page.css('.quote .text::text')
print(f"找到 {len(quotes)} 条名言")
# 输出: 找到 10 条名言
print(f"第一条名言: {quotes[0]}")