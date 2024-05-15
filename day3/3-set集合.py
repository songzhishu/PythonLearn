# set集合
# 创建set集合
s = {1, 2, "2", 3, 4, 5}
print(s)  # 输出: {1, 2, 3, 4, 5}

# 创建空集合
k = set()
print(k)

# 创建set集合
set = {1, 2, 3, 4, 5}

# 添加元素
set.add(6)
print(set)  # 输出: {1, 2, 3, 4, 5, 6}

# 删除元素
set.remove(1)
print(set)  # 输出: {2, 3, 4, 5, 6}

# 随机取出一个元素
print(set.pop())

# 清空集合
set.clear()
print(set)  # 输出: set()

# 判断元素是否在集合中
print(1 in set)  # 输出: False

# 集合的交集
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
print(set1 & set2)  # 输出: {4, 5}
difference = set1.difference(set2)
print(difference)  # 输出: {1, 2, 3}
# 集合的并集
print(set1 | set2)  # 输出: {1, 2, 3, 4, 5, 6, 7, 8}
union = set1.union(set2)
print(union)

update = set1.intersection_update(set2)
print(update)  # 集合的差集
