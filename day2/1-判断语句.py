# 定义一个字典
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

# 使用for循环遍历字典
for key, value in my_dict.items():
    print(f"{key}: {value}")

# 真假判断
k = True
if k:
    print("k是真")
else:
    print("k是假")

# 判断
if int(input()) > 18:
    # 输出True
    print("你好,你已经成年了,需要补交税款")
    print("不好意哦,你已经成年了,需要补交税款")
else:
    # 输出False
    print("你好,你还未成年,不需要补交税款")
print("你好")

# 输入成绩
score = int(input("请输入成绩："))

# 判断成绩
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")

elif score >= 70:
    print("中等")

elif score >= 60:
    print("及格")

else:
    print("不及格")
