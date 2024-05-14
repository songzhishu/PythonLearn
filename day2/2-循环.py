# 猜数字
# 随机一个1到100之间的数字
import random

number = random.randint(1, 100)
print("游戏开始！")
# 可以猜6次
for i in range(6):
    key = int(input("请输入你猜的数字："))
    if key > number:
        print(f"猜大了！还有{5 - i}次机会")
        if i == 5:
            print(f"很遗憾，你没有猜对答案是:{number}")

    elif key < number:
        print(f"猜小了！还有{5 - i}次机会")
        if i == 5:
            print(f"很遗憾，你没有猜对答案是:{number}")

    elif key == number:
        print(f"恭喜你，猜对了答案是:{number}")
