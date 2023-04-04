import hashlib


def hash_password(password):
    # 将密码转换为字节串
    password_bytes = password.encode('utf-8')
    # 使用 md5 算法进行加密
    hash_obj = hashlib.md5(password_bytes)
    # 返回加密后的结果
    return hash_obj.hexdigest()
