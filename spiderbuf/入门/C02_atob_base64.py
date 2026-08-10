import base64
import json

encrypted_data = "ewogICAgICAiZmxpZ2h0cyI6IFsKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljJfkuqwiLCAicHJpY2UiOiA4MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLkuIrmtbciLCAicHJpY2UiOiA3NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmiJDpg70iLCAicHJpY2UiOiA3MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmt7HlnLMiLCAicHJpY2UiOiAyMDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmna3lt54iLCAicHJpY2UiOiA2NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljZfkuqwiLCAicHJpY2UiOiA2MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLph43luoYiLCAicHJpY2UiOiA3MjAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLopb/lrokiLCAicHJpY2UiOiA2ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmmIbmmI4iLCAicHJpY2UiOiA2MjAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmrabmsYkiLCAicHJpY2UiOiA1MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLplb/mspkiLCAicHJpY2UiOiA0ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljqbpl6giLCAicHJpY2UiOiA0NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLpnZLlspsiLCAicHJpY2UiOiA3ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlpKnmtKUiLCAicHJpY2UiOiA3MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmsojpmLMiLCAicHJpY2UiOiA4NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlpKfov54iLCAicHJpY2UiOiA4MzAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlk4jlsJTmu6giLCAicHJpY2UiOiA5MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLkuInkupoiLCAicHJpY2UiOiA1NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLnj6DmtbciLCAicHJpY2UiOiAxODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmoYLmnpciLCAicHJpY2UiOiA0MDAgfQogICAgICBdCiAgICB9"

# Base64 解码
decoded = base64.b64decode(encrypted_data).decode('utf-8')
data = json.loads(decoded)
print(data)

# 打印航班信息
print("航班列表:")
for flight in data['flights']:
    print(f"  {flight['from']} → {flight['to']} : ¥{flight['price']}")

# 生成 HTML 表格
html = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>航班列表</title></head>
<body>
<table border="1">
    <thead><tr><th>出发地</th><th>目的地</th><th>价格(元)</th></tr></thead>
    <tbody>
"""

for flight in data['flights']:
    html += f"        <tr><td>{flight['from']}</td><td>{flight['to']}</td><td>{flight['price']}</td></tr>\n"

html += """    </tbody>
</table>
</body>
</html>
"""

with open('flights.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\n已生成 flights.html 文件")
sum_ = 0
count = 0
for flight in data['flights']:
    sum_ += flight['price']
    count += 1
print(sum_ / count)