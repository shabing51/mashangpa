import numpy as np
import pandas as pd

# a = pd.Series([52.75, 48.20, -2.5])
# a_int = a.astype(np.int64) # 仅保留整数部分  astype(np.int64) 执行向零取整
# print(a_int)
# """
# 0    52
# 1    48
# 2    -2
# dtype: int64
# """

# # 任何数 & 全1 = 该数本身（在32位范围内）
# x = 52
# print(x & 0xFFFFFFFF)  # 52
#
# # 超出32位的数会被截断
# x = 2**33  # 8589934592 (33位)
# print(x & 0xFFFFFFFF)  # 0 (只保留低32位)
#
# # 负数的处理
# x = -2   # python ...11111111 11111111 11111111 11111110（无限个1，然后...1110）
# print(x & 0xFFFFFFFF)  # 4294967294  11111111 11111111 11111111 11111110



# # 用8位代替32位说明
# # 8位无符号范围：0-255
# # 8位有符号范围：-128 到 127
# def to_int8(x):
#     """8位版本的转换（简化示例）"""
#     uint8 = x & 0xFF  # 0xFF = 255
#     if uint8 > 0x7F:  # 0x7F = 127
#         return uint8 - 0x100  # 0x100 = 256
#     return uint8
# """
# 有符号值 = 无符号值 - 256  (当无符号值 >= 128)
# 有符号值 = 无符号值        (当无符号值 <  128)
# """
# # Test
# print(to_int8(-1))   # -1  (255 → -1)
# print(to_int8(-2))   # -2  (254 → -2)
# print(to_int8(127))  # 127
# print(to_int8(128))  # -128 (128 → -128)
# print(to_int8(255))  # -1


# 有符号和无符号是模 256 的同一个剩余类
# 只是选择了不同的代表元
# 无符号选择 [0, 255] 作为代表
# 有符号选择 [-128, 127] 作为代表
# 转换就是切换代表元
def convert_to_signed(unsigned, bits=8):
    modulus = 2 ** bits
    half = modulus // 2
    if unsigned >= half:
        return unsigned - modulus
    return unsigned

# Test
print(convert_to_signed(255, 8))   # -1
print(convert_to_signed(254, 8))   # -2
print(convert_to_signed(128, 8))   # -128
print(convert_to_signed(127, 8))   # 127


"""
负数 + 正数 = 0（自然溢出）
(-1) + 1 = 0
# 如果用 11111111 表示 -1
  11111111  (-1)
+ 00000001  (1)
= 00000000  (0)  # 进位丢弃，正好是0

1 的 8 位二进制 = 00000001
设 (-1) 的二进制为 x, ==> x + 00000001 = 00000000 (8位)
那么 x = 00000000 - 00000001
...

负数的补码 = 正数取反 + 1  # 计算机使用补码表示负数的结果
# 对于任意正数 n
n 的二进制 = 某数
取反 = 所有位翻转
n + 取反(n) = 11111111 (全1)
再加 1：
n + (取反(n) + 1) = 00000000 (进位溢出)


# 255 + 1 = 256 → 0 (溢出)
# -1 + 1 = 0
==> 255 to -1 


8位二进制就像一个圆盘
想象一个只有 256 个刻度的圆盘（0 到 255）: 类时钟
        0
   255      1
254          2
   .          3
   .           4
   .         ...   
130         126
   129    127
       128
从 0 开始，顺时针走 255 步 → 到达 255
从 0 开始，逆时针走 1 步 → 也到达 255
所以 255 和 -1 在圆盘上是同一个位置！
模 256 剩余类
"""
print(int(-5.3))  # ==> -5 向零取整,只要整数部分
print(int(-5.3) == -int(--5.3)) # True
print(0xFFFFFFFF//2 == 0x7FFFFFFF == 0xFFFFFFFF>>1) # True
print(-1//2)  # -1
print(0x100000000 == 16**8)  # True, (2^4)^8 = 2^32

import string
print(string.ascii_lowercase)
print(string.digits)
print(string.punctuation) # 标点符号