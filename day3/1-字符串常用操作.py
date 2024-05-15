str = "你 好 世界 这是 一个 测试 用来测试 字符串 的 常用 操作"

# 查看初始字符串的索引位置
index = str.index("测试")
print(index)

# 替换字符串中的部分内容
new_str = str.replace("测试", "替换")
print(new_str)

# 查找字符串中是否包含指定的子串
result = str.find("测试")
print(result)

# 统计字符串中指定子串出现的次数
count = str.count("测试")
print(count)

# 分割字符串
split_str = str.split(" ")
print(split_str)


