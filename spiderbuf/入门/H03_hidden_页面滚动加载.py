"""
window.addEventListener('scroll', function () {
    const pageHeight = document.body.scrollHeight;
    const windowHeight = window.innerHeight;
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

    const threshold = 100;
    if (pageHeight - (windowHeight + scrollTop) < threshold) {
        var page = document.getElementById('sLaOuol2SM0iFj4d');
        if (page == null) {
            return;
        }
        fetch("./h03/" + page.textContent).then(response => response.text())
        .then(function (data) {
            var main_div = document.getElementById('main');
            page.remove();
            main_div.insertAdjacentHTML("beforeEnd", data);
        });
    }
});

<div id="sLaOuol2SM0iFj4d" hidden>5f685274073b</div>
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://spiderbuf.cn/web-scraping-practices/6?order=rating",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
cookies = {
    "_ga": "GA1.1.556439622.1775108645",
    "_ga_7B42BKG1QE": "GS2.1.s1775208382$o14$g1$t1775212351$j60$l0$h0"
}


def get_hidden_text(url_):
    response = requests.get(url_, headers=headers, cookies=cookies)

    soup = BeautifulSoup(response.text, "lxml")
    # print(soup.prettify())  # 美化HTML|XML

    hidden = soup.select_one("#sLaOuol2SM0iFj4d")
    return hidden.text if hidden else ''

base_url = "https://spiderbuf.cn/web-scraping-practice/scraping-scroll-load/"
hidden_txt = get_hidden_text(base_url)
resp = requests.get(base_url, headers=headers, cookies=cookies)
data = resp.text
print(hidden_txt)
while hidden_txt != "" :
    url = base_url + hidden_txt
    resp = requests.get(url, headers=headers, cookies=cookies)
    data += resp.text
    print("="*100)
    hidden_txt = get_hidden_text(url)
    print(hidden_txt)

print(data)



