money = 5000000


def nquire(flag):
    if flag:
        print("-------------------查询余额--------------------")
        print("您的余额为:", money)
    else:
        print("您的余额为:", money)


def deposit(k):
    global money
    money += k
    print("-------------------存款--------------------")
    print("存款成功")
    nquire(False)


def withdrawal(k):
    global money
    if k > money:
        print("-------------------取款--------------------")
        print("余额不足")
    else:
        money -= k
        print("-------------------取款--------------------")
        print("取款成功")
        nquire(False)


def zhucun():
    print("-------------------主菜单--------------------")
    print("1. 查询余额")
    print("2. 存款")
    print("3. 取款")
    print("4. 退出")
    print("请输入您的操作:")
    s = input()
    if s == "1":
        nquire(True)
    elif s == "2":
        k = int(input("请输入存款金额:"))
        deposit(k)

    elif s == "3":
        k = int(input("请输入取款金额:"))
        withdrawal(k)

    elif s == "4":
        print("-------------------退出--------------------")
        print("感谢使用本系统")
        exit()
    else:
        print("输入错误，请重新输入")

while True:
    zhucun()
