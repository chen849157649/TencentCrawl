from hashlib import sha1


def get_hash(str):
    sh = sha1()
    # 更新哈希对象,以字符串为参数
    sh.update(str.encode('utf8'))
    # 返回密码，作为十六进制数据字符串值
    return sh.hexdigest()