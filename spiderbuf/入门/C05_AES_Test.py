from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# ========== AES-CBC 模式 ==========
def aes_cbc_example():
    # 生成密钥（32字节 = AES-256）
    # os.urandom()返回的是bytes对象
    key = os.urandom(32)
    iv = os.urandom(16)  # 初始化向量
    print("key: ", key)  # b'\x97\x8a\xfb\xddfc\xb4\xd5lX\xba\x96\xac\x96\xa3\x13IO\x1d[\x05\x06oZI\x9e\x1f\xa3\x81\x82c '
    print("iv: ", iv)    # b'\x1f\xf3\xc4\xa8q\xb7y\x9dv\x11y9$<\xd7\xb6'
    # 创建加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 需要加密的数据（必须是16的倍数）
    plaintext = b"This is a secret message!!"
    # 填充到16的倍数
    pad_length = 16 - (len(plaintext) % 16)
    plaintext_padded = plaintext + bytes([pad_length]) * pad_length

    ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()

    # 解密
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # 去除填充
    pad_len = decrypted_padded[-1]
    decrypted = decrypted_padded[:-pad_len]

    print(f"原始数据: {plaintext}")
    print(f"加密后: {ciphertext.hex()}")
    print(f"解密后: {decrypted}")


# ========== AES-GCM 模式（推荐，自带认证）==========
def aes_gcm_example():
    key = os.urandom(32)  # AES-256
    iv = os.urandom(12)  # GCM推荐12字节
    plaintext = b"Confidential data"
    aad = b"additional authenticated data"  # 可选认证数据

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(aad)

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag  # 认证标签

    # 解密并验证
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(aad)
    decrypted = decryptor.update(ciphertext) + decryptor.finalize_with_tag(tag)

    print(f"GCM加密结果: {ciphertext.hex()}")
    print(f"认证标签: {tag.hex()}")
    print(f"解密验证: {decrypted}")


# ========== AES-CTR 模式 ==========
def aes_ctr_example():
    key = os.urandom(32)
    nonce = os.urandom(8)  # 随机数
    counter = 0  # 计数器起始值

    cipher = Cipher(
        algorithms.AES(key),
        modes.CTR(nonce + counter.to_bytes(8, 'big')),
        backend=default_backend()
    )

    plaintext = b"Stream cipher example"
    print("plaintext: ", plaintext)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    print(f"CTR模式: {decrypted}")


# ========== AES-ECB(不安全) 模式 ==========
# ========== ECB 模式实现 =================
def aes_ecb_example():
    # 生成密钥（16/24/32字节）
    key = os.urandom(32)  # AES-256
    plaintext = b"Hello ECB mode!!!"

    # ECB 模式不需要 IV，直接传入 None
    cipher = Cipher(
        algorithms.AES(key),
        modes.ECB(),  # ECB 模式不需要参数
        backend=default_backend()
    )

    # 加密
    encryptor = cipher.encryptor()

    # 数据必须是16的倍数，需要手动填充
    padded_plaintext = pad_data(plaintext)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # 解密
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted = unpad_data(decrypted_padded)

    print(f"密钥: {key.hex()}")
    print(f"明文: {plaintext}")
    print(f"密文: {ciphertext.hex()}")
    print(f"解密: {decrypted}")

    return ciphertext


# ========== 填充函数（PKCS7）==========
def pad_data(data: bytes, block_size: int = 16) -> bytes:
    """PKCS7 填充"""
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length]) * padding_length


def unpad_data(data: bytes) -> bytes:
    """去除 PKCS7 填充"""
    padding_length = data[-1]
    return data[:-padding_length]


# ========== 演示 ECB 模式的安全问题 ==========
def demonstrate_ecb_problem():
    """演示为什么 ECB 不安全"""
    from PIL import Image
    import numpy as np

    key = os.urandom(32)

    # 创建简单的测试数据
    # 重复的明文块
    plaintext1 = b"AAAAAAAAAAAAAAAA"  # 16字节全是A
    plaintext2 = b"BBBBBBBBBBBBBBBB"  # 16字节全是B
    plaintext3 = b"AAAAAAAAAAAAAAAA"  # 与plaintext1相同

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 加密相同的明文块
    ct1 = encryptor.update(plaintext1)
    ct2 = encryptor.update(plaintext2)

    # 重新创建加密器（演示用）
    encryptor2 = cipher.encryptor()
    ct3 = encryptor2.update(plaintext3)

    print("\n=== ECB 安全问题演示 ===")
    print(f"明文1 (16个A): {plaintext1}")
    print(f"密文1: {ct1.hex()}")
    print(f"明文2 (16个B): {plaintext2}")
    print(f"密文2: {ct2.hex()}")
    print(f"明文3 (16个A): {plaintext3}")
    print(f"密文3: {ct3.hex()}")
    print(f"密文1 == 密文3: {ct1 == ct3}")  # True! 相同明文产生相同密文
    print("这暴露了数据模式！")


# ========== 加密文件（不推荐用于生产）==========
def ecb_encrypt_file(key: bytes, input_file: str, output_file: str):
    """使用 ECB 加密文件（演示用）"""
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            while True:
                chunk = f_in.read(16)  # 一次读16字节
                if not chunk:
                    break
                if len(chunk) < 16:
                    # 填充最后一个块
                    chunk = pad_data(chunk)
                encrypted_chunk = encryptor.update(chunk)
                f_out.write(encrypted_chunk)
            f_out.write(encryptor.finalize())


def ecb_decrypt_file(key: bytes, input_file: str, output_file: str):
    """解密 ECB 加密的文件"""
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            while True:
                chunk = f_in.read(16)
                if not chunk:
                    break
                decrypted_chunk = decryptor.update(chunk)
                if len(decrypted_chunk) == 16:
                    # 最后一个块需要去除填充
                    if f_in.peek(1):  # 还有更多数据
                        f_out.write(decrypted_chunk)
                    else:
                        # 最后一个块，去除填充
                        f_out.write(unpad_data(decrypted_chunk))
                else:
                    f_out.write(decrypted_chunk)



if __name__ == "__main__":
    # # aes_ecb_Test
    # aes_ecb_example()
    #
    # # 演示安全问题
    # demonstrate_ecb_problem()

    # 文件加密（不推荐）
    # key = os.urandom(32)
    # ecb_encrypt_file(key, "original.txt", "encrypted.ecb")
    # ecb_decrypt_file(key, "encrypted.ecb", "decrypted.txt")

    pass

# print("==================aes_gcm_example()=======================")
# aes_gcm_example()
# print("\n")
# print("==================aes_cbc_example()=======================")
# aes_cbc_example()
# print("\n")
# print("==================aes_ctr_example()=======================")
# aes_ctr_example()



# 下面这个是新手友好的,几行代码搞定, pycryptodome
"""
pip install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple 

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# AES-CBC 模式
key = get_random_bytes(32)  # AES-256
cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(b"Secret message", AES.block_size))

# 解密
decipher = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)
print(f"解密结果: {plaintext}")

# AES-GCM 模式（推荐）
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(b"Important data")

# 解密
decipher = AES.new(key, AES.MODE_GCM, cipher.nonce)
decrypted = decipher.decrypt_and_verify(ciphertext, tag)
"""
