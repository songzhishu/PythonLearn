def my_len(str):
    count = 0
    for i in str:
        count += 1
    return count


s = input("请输入一个字符串：")
print("输入的长度:%d" % my_len(s))


def my_sum(*args):
    sum = 0
    for i in args:
        sum += i
    return sum


i = my_sum(1, 2, 3, 4, 5)
print("i = ", i)


def my_add(a, b):
    """
    这是一个求和函数
    :param a:
    :param b:
    :return:
    """
    return a + b


i = my_add(1, 2)
print("i = ", i)


