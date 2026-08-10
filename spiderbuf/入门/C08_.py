import base64
import hashlib
import requests
import hmac,time,json
from Crypto.Cipher import AES


def get_financial_data():
    """
    爬取 C08 页面的金融数据
    """
    # 1. 配置
    base_url = "https://spiderbuf.cn/web-scraping-practice/scraper-practice-c08"

    # 2. 生成请求参数
    timestamp = int(time.time())
    timestamp_str = str(timestamp)

    # 生成 salt（模拟 performance.now()）
    salt_raw = '{:.6f}'.format(time.perf_counter() * 1000)
    salt = base64.b64encode(salt_raw.encode()).decode()
    # print(base64.b64encode(salt_raw.encode()))  b'xxxxxxxxxxx'
    # 生成签名
    message = (salt + timestamp_str).encode()
    signature = hmac.new(base_url.encode(), message, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()

    print(f"Timestamp: {timestamp}")
    print(f"Salt: {salt}")
    print(f"Signature: {signature_b64}")

    # 3. 发送请求
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referer": base_url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "cache-control": "no-cache",
    }

    params = {
        "t": timestamp_str,
        "s": salt,
        "sig": signature_b64,
    }

    response = requests.get(f"{base_url}/api", headers=headers, params=params)
    print(f"状态码: {response.status_code}")

    if response.status_code != 200:
        print(f"请求失败: {response.text}")
        return None

    # 4. 解密响应数据
    result = response.json()
    cipher_data = base64.b64decode(result['d'])

    # 密钥：signature 的前16字节
    key = signature_b64[:16].encode('utf-8')

    # IV：密文的前16字节
    iv = cipher_data[:16]
    ciphertext = cipher_data[16:]

    print(f"密钥: {key}")
    print(f"IV长度: {len(iv)}")
    print(f"密文长度: {len(ciphertext)}")

    # AES-CBC 解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    # 去除 PKCS7 填充
    pad_len = decrypted[-1]
    if pad_len <= 16:
        decrypted = decrypted[:-pad_len]

    # 解析 JSON
    raw = decrypted.decode('utf-8')
    items = json.loads(raw)

    return items


def calculate_average_price(data):
    """
    计算 Price 列的平均值
    """
    if not data:
        return None

    total = 0
    count = 0

    for item in data:
        # 根据实际数据结构获取价格
        price = item.get('price') or item.get('Price') or item.get('current_price')
        if price is not None:
            total += float(price)
            count += 1

    if count == 0:
        return None

    average = total / count
    return average


def display_data(data):
    """
    显示数据表格
    """
    if not data:
        print("没有数据")
        return

    print("\n" + "=" * 120)
    print("金融数据列表")
    print("=" * 120)

    # 打印表头
    if len(data) > 0:
        headers = list(data[0].keys())
        print(" | ".join(f"{h:^15}" for h in headers))
        print("-" * 120)

        # 打印数据
        for item in data[:20]:  # 只显示前20条
            row = [f"{str(item.get(h, '')):^15}" for h in headers]
            print(" | ".join(row))

    print(f"\n共 {len(data)} 条数据")


def main():
    print("=" * 60)
    print("爬虫实战练习 C08 - 金融数据爬取")
    print("=" * 60)

    # 获取数据
    data = get_financial_data()

    if data:
        # 显示数据
        display_data(data)

        # 计算平均值
        average = calculate_average_price(data)
        if average is not None:
            print("\n" + "=" * 60)
            print(f"Price 列的平均值: {average:.2f}")
            print("=" * 60)
        else:
            print("\n未找到 Price 字段")

        # # 保存到文件
        # with open('financial_data.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, indent=2, ensure_ascii=False)
        # print("\n数据已保存到 financial_data.json")

        # # 保存为 CSV
        # import csv
        # if data:
        #     with open('financial_data.csv', 'w', newline='', encoding='utf-8') as f:
        #         writer = csv.DictWriter(f, fieldnames=data[0].keys())
        #         writer.writeheader()
        #         writer.writerows(data)
        #     print("数据已保存到 financial_data.csv")
    else:
        print("获取数据失败")


if __name__ == "__main__":
    main()