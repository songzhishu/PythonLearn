word = [1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 22, 45, 999, 5, 5, 69, 54, 9, 45, 9, 95, 1, 8,
        9, 28, 9, 5, 8, 7, 5, 13, 14, 15, 16, 17, 18, 19, 20]

# 查询 是否存在
index = word.index(3)
print(index)

# 修改
word[0] = 100
print(word)

# 插入 插入位置 参数
word.insert(0, 1000)
print(word)

# 添加
word.append(200)
print(word)

# 删除 根据值删除
word.remove(200)
print(word)

# 删除 根据索引删除
word.pop(0)
print(word)

del word[0]
print(word)

# 切片
print(word[0:4])

# 统计
print(word.count(3))

# 排序
word.sort()
print(word)

# 反转
word.reverse()
print(word)

# 去重
word = list(set(word))
print(word)

# 添加列表
word.extend([1, 2, 3, 4, 5])
print(word)
