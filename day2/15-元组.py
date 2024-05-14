# 一旦定义完成，元组就不能修改

# 定义一个元组
my_tuple = (1, 2, 3, 4, 5)

# 尝试修改元组
# my_tuple[0] = 10   修改操作会引发TypeError异常
print(type(my_tuple))

# 定义单个元素的元组
my_tuple1 = (1, 2, 3, 4, 5)  # 需要在元素后添加逗号
print(my_tuple1)

# 定义空元组
my_tuple2 = (my_tuple, my_tuple1)
print(my_tuple2)

i = my_tuple2[1][2]
print(i)

# 遍历元组
for i in my_tuple:
    print(i)

# 获取元组长度
print(len(my_tuple))

# 检查元素是否在元组中
print(1 in my_tuple)

# 连接元组
my_tuple3 = my_tuple + my_tuple1
print(my_tuple3)

# 访问元组中的元素
print(my_tuple3[0])

# 查找元组中的元素的小标
print(f"下标:{my_tuple.index(3)}")

# 获取元组中的最大值
print(max(my_tuple3))

# 获取元组中的最小值
print(min(my_tuple3))

# 获取元组中的元素个数
print(my_tuple3.count(1))

# 判断元组是否为空
print(not my_tuple3)

# 判断元组是否不为空
print(my_tuple3)


# 添加元素到元组
my_tuple4 = my_tuple3 + (6, 7, 8)
print(my_tuple4)