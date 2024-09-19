import random
import string

def generate_password(length=8):
    """生成一个指定长度的随机密码"""
    characters = string.ascii_letters + string.digits  # 包括大小写字母和数字
    return ''.join(random.choice(characters) for _ in range(length))

def generate_passwords(num_passwords, length=8):
    """生成指定数量的随机密码"""
    passwords = set()  # 使用集合来避免重复密码
    while len(passwords) < num_passwords:
        passwords.add(generate_password(length))
    return list(passwords)

def save_passwords_to_file(passwords, filename):
    """将密码列表保存到文件中"""
    with open(filename, 'w') as f:
        for password in passwords:
            f.write(password + '\n')

# 参数设置
num_passwords = 100000  # 需要生成的密码数量
password_length = 8  # 密码长度

# 生成密码并保存到文件
passwords = generate_passwords(num_passwords, password_length)
save_passwords_to_file(passwords, 'passwords.txt')
