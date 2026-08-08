from curl_cffi import requests

def get_data_by_page_num(page_num, session):
    params = {
        'page': str(page_num),
    }
    resp = session.get(('https://www.mashangpa.com'
                        '/api/problem-detail/3/data/'), 
                        params=params)
    resp.raise_for_status()

    return resp.json()['current_array']


def main():
    print(f"".center(62, '='))
    total = 0

    cookies = { ##需要更换 sessionid
        'sessionid': '7jkdu0y5c22e0vd7bca2ybusg7qhdgjs',
    }
    headers = {
        'pragma': 'no-cache',
        'referer': 'https://www.mashangpa.com/problem-detail/3/',
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/151.0.0.0 Safari/537.36'),
    }
    session = requests.Session(headers=headers, cookies=cookies)

    for page_num in range(1, 21):
        current_array = get_data_by_page_num(page_num, session)
        print(f"第{page_num:2d}页数据: {current_array}")
    
        total = total + sum(current_array)
    print(f"20页数据的和: {total} ".center(56, '='))

if __name__ == "__main__":
    main()

