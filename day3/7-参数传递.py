# 位置参数 就是按照顺序传递参数
def say_hello(name, age):
    print(f"你好，{name}，你今年{age}岁了")


say_hello("张三", 20)

# 关键字参数 就是按照参数名传递参数 顺序可以不指定
say_hello(name="李四", age=24)


# 默认参数 就是设置一个默认值，当不传递参数时，使用默认值
def say_hello(name, age=18): # 默认参数必须放在最后
    print(f"你好，{name}，你今年{age}岁了")


say_hello("张三")
say_hello("李四", 24)


# 收集参数 就是收集传递的所有参数，并放在一个元组中
def say_hello(*args):
    print(args)


say_hello("张三", 20, "男")


# 函数作为参数传递
def say_hello(name, age):
    print(f"你好，{name}，你今年{age}岁了")


def say_goodbye(func):
    print("再见")
    func("张三", 20)


say_goodbye(say_hello)