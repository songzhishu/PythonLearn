# 多个函数返回值

def get_user_info():
    name = input("请输入用户名：")
    pwd = input("请输入密码：")
    return name, pwd


def login(name, pwd):
    if name == "admin" and pwd == "123456":
        return True, "登录成功"
    else:
        return False, "用户名或密码错误"


# 调用函数获取用户输入
user_info = get_user_info()

# 调用login函数进行验证
result = login(user_info[0], user_info[1])

# 输出结果
if result[0]:
    print(result[1])
    # 登录成功后可以继续执行其他操作
else:
    print(result[1])