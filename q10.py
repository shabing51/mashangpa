from curl_cffi import requests
import execjs
import hashlib
import struct
import hashlib
# md5算法的初始向量顺序被交换了！
# sha256(md5_modified(param))
def md5_modified(data: str) -> str:
    """自定义 MD5 变种 - 初始向量顺序不同"""
    def left_rotate(x, n):
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    
    def h_add(a, b):
        # 对应 JavaScript 中的 h 函数
        a &= 0xFFFFFFFF
        b &= 0xFFFFFFFF
        
        # 检查最高位
        a_high = (a >> 31) & 1
        b_high = (b >> 31) & 1
        
        # 检查第 30 位
        a_mid = (a >> 30) & 1
        b_mid = (b >> 30) & 1
        
        # 低 30 位相加
        sum_low = (a & 0x3FFFFFFF) + (b & 0x3FFFFFFF)
        
        if a_mid and b_mid:
            return (sum_low ^ 0x80000000 ^ (a_high << 31) ^ (b_high << 31)) & 0xFFFFFFFF
        elif a_mid or b_mid:
            if sum_low & 0x40000000:
                return (sum_low ^ 0xC0000000 ^ (a_high << 31) ^ (b_high << 31)) & 0xFFFFFFFF
            else:
                return (sum_low ^ 0x40000000 ^ (a_high << 31) ^ (b_high << 31)) & 0xFFFFFFFF
        else:
            return (sum_low ^ (a_high << 31) ^ (b_high << 31)) & 0xFFFFFFFF
    
    def k(a, b, c, d, x, s, t):
        # 对应 JavaScript 中的 k 函数
        f = (b & c) | ((~b) & d)
        a = h_add(a, h_add(h_add(f, x), t))
        a = h_add((a << s) | (a >> (32 - s)), b)
        return a & 0xFFFFFFFF
    
    def l(a, b, c, d, x, s, t):
        # 对应 JavaScript 中的 l 函数
        f = (b & d) | (c & (~d))
        a = h_add(a, h_add(h_add(f, x), t))
        a = h_add((a << s) | (a >> (32 - s)), b)
        return a & 0xFFFFFFFF
    
    def m_func(a, b, c, d, x, s, t):
        # 对应 JavaScript 中的 m 函数
        f = b ^ c ^ d
        a = h_add(a, h_add(h_add(f, x), t))
        a = h_add((a << s) | (a >> (32 - s)), b)
        return a & 0xFFFFFFFF
    
    def n(a, b, c, d, x, s, t):
        # 对应 JavaScript 中的 n 函数
        f = c ^ (b | (~d))
        a = h_add(a, h_add(h_add(f, x), t))
        a = h_add((a << s) | (a >> (32 - s)), b)
        return a & 0xFFFFFFFF
    
    msg = data.encode('utf-8')
    original_len = len(msg)
    
    # 填充
    msg = bytearray(msg)
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0x00)
    
    # 添加长度（位）
    bit_len = original_len * 8
    msg.extend(struct.pack('<Q', bit_len))
    
    # 初始向量（自定义顺序！）
    A = 0x10325476  # 标准 MD5 的 D
    B = 0x98BADCFE  # 标准 MD5 的 C
    C = 0xEFCDAB89  # 标准 MD5 的 B
    D = 0x67452301  # 标准 MD5 的 A
    
    # 处理 512 位块
    for i in range(0, len(msg), 64):
        block = msg[i:i+64]
        words = list(struct.unpack('<16I', block))
        
        a, b, c, d = A, B, C, D
        
        # 第 1 轮 (k)
        a = k(a, b, c, d, words[0], 7, 0xD76AA478)
        d = k(d, a, b, c, words[1], 12, 0xE8C7B756)
        c = k(c, d, a, b, words[2], 17, 0x242070DB)
        b = k(b, c, d, a, words[3], 22, 0xC1BDCEEE)
        a = k(a, b, c, d, words[4], 7, 0xF57C0FAF)
        d = k(d, a, b, c, words[5], 12, 0x4787C62A)
        c = k(c, d, a, b, words[6], 17, 0xA8304613)
        b = k(b, c, d, a, words[7], 22, 0xFD469501)
        a = k(a, b, c, d, words[8], 7, 0x698098D8)
        d = k(d, a, b, c, words[9], 12, 0x8B44F7AF)
        c = k(c, d, a, b, words[10], 17, 0xFFFF5BB1)
        b = k(b, c, d, a, words[11], 22, 0x895CD7BE)
        a = k(a, b, c, d, words[12], 7, 0x6B901122)
        d = k(d, a, b, c, words[13], 12, 0xFD987193)
        c = k(c, d, a, b, words[14], 17, 0xA679438E)
        b = k(b, c, d, a, words[15], 22, 0x49B40821)
        
        # 第 2 轮 (l)
        a = l(a, b, c, d, words[1], 5, 0xF61E2562)
        d = l(d, a, b, c, words[6], 9, 0xC040B340)
        c = l(c, d, a, b, words[11], 14, 0x265E5A51)
        b = l(b, c, d, a, words[0], 20, 0xE9B6C7AA)
        a = l(a, b, c, d, words[5], 5, 0xD62F105D)
        d = l(d, a, b, c, words[10], 9, 0x02441453)
        c = l(c, d, a, b, words[15], 14, 0xD8A1E681)
        b = l(b, c, d, a, words[4], 20, 0xE7D3FBC8)
        a = l(a, b, c, d, words[9], 5, 0x21E1CDE6)
        d = l(d, a, b, c, words[14], 9, 0xC33707D6)
        c = l(c, d, a, b, words[3], 14, 0xF4D50D87)
        b = l(b, c, d, a, words[8], 20, 0x455A14ED)
        a = l(a, b, c, d, words[13], 5, 0xA9E3E905)
        d = l(d, a, b, c, words[2], 9, 0xFCEFA3F8)
        c = l(c, d, a, b, words[7], 14, 0x676F02D9)
        b = l(b, c, d, a, words[12], 20, 0x8D2A4C8A)
        
        # 第 3 轮 (m)
        a = m_func(a, b, c, d, words[5], 4, 0xFFFA3942)
        d = m_func(d, a, b, c, words[8], 11, 0x8771F681)
        c = m_func(c, d, a, b, words[11], 16, 0x6D9D6122)
        b = m_func(b, c, d, a, words[14], 23, 0xFDE5380C)
        a = m_func(a, b, c, d, words[1], 4, 0xA4BEEA44)
        d = m_func(d, a, b, c, words[4], 11, 0x4BDECFA9)
        c = m_func(c, d, a, b, words[7], 16, 0xF6BB4B60)
        b = m_func(b, c, d, a, words[10], 23, 0xBEBFBC70)
        a = m_func(a, b, c, d, words[13], 4, 0x289B7EC6)
        d = m_func(d, a, b, c, words[0], 11, 0xEAA127FA)
        c = m_func(c, d, a, b, words[3], 16, 0xD4EF3085)
        b = m_func(b, c, d, a, words[6], 23, 0x04881D05)
        a = m_func(a, b, c, d, words[9], 4, 0xD9D4D039)
        d = m_func(d, a, b, c, words[12], 11, 0xE6DB99E5)
        c = m_func(c, d, a, b, words[15], 16, 0x1FA27CF8)
        b = m_func(b, c, d, a, words[2], 23, 0xC4AC5665)
        
        # 第 4 轮 (n)
        a = n(a, b, c, d, words[0], 6, 0xF4292244)
        d = n(d, a, b, c, words[7], 10, 0x432AFF97)
        c = n(c, d, a, b, words[14], 15, 0xAB9423A7)
        b = n(b, c, d, a, words[5], 21, 0xFC93A039)
        a = n(a, b, c, d, words[12], 6, 0x655B59C3)
        d = n(d, a, b, c, words[3], 10, 0x8F0CCC92)
        c = n(c, d, a, b, words[10], 15, 0xFFEFF47D)
        b = n(b, c, d, a, words[1], 21, 0x85845DD1)
        a = n(a, b, c, d, words[8], 6, 0x6FA87E4F)
        d = n(d, a, b, c, words[15], 10, 0xFE2CE6E0)
        c = n(c, d, a, b, words[6], 15, 0xA3014314)
        b = n(b, c, d, a, words[13], 21, 0x4E0811A1)
        a = n(a, b, c, d, words[4], 6, 0xF7537E82)
        d = n(d, a, b, c, words[11], 10, 0xBD3AF235)
        c = n(c, d, a, b, words[2], 15, 0x2AD7D2BB)
        b = n(b, c, d, a, words[9], 21, 0xEB86D391)
        
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF
    
    def to_hex(value):
        result = ''
        for i in range(4):
            byte = (value >> (8 * i)) & 0xFF
            result += f'{byte:02x}'
        return result
    
    return (to_hex(A) + to_hex(B) + to_hex(C) + to_hex(D)).lower()

def get_t(pageNum):
    url = f"/api/problem-detail/10/data/?page={pageNum}"
    suffix = "b|s|b|s|b|s|b|s|b|l"
    combined = url + suffix

    t = hashlib.sha256(
        md5_modified(combined).encode('utf-8')
    ).hexdigest()
    return t



with open('./q10.cjs', 'r', encoding='utf8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)
url = 'https://www.mashangpa.com/api/problem-detail/10/data/'

print(f"".center(62, '='))
total = 0
for  ii in range(1, 21, 1):
    # t = ctx.call('OOOO', f"/api/problem-detail/10/data/?page={ii}")
    t = get_t(ii) 
    params = {
        "page": str(ii),
        "t": t
    }
    # print(t)
    r = requests.get(url, params=params, 
                        verify=False, 
                        cookies={
                            "sessionid": 
                            "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs"
                        }
                    )
    data_list = r.json().get('current_array', [])
    print(f"第{ii:02d}页数据: {data_list}")
    total += sum(data_list)

print(f"20页数据的和: {total} ".center(56, '='))
