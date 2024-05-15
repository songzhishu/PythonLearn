# 定义字典
ds = {'name': '张三', 'age': 20, 'gender': '男'}

# 访问字典中的值
print(ds['name'])  # 输出：张三
print(ds['age'])  # 输出：20
print(ds['gender'])  # 输出：男

# 修改字典中的值
ds['age'] = 25
print(ds)

# 添加新的键值对
ds['address'] = '北京'
print(ds)  # 输出：北京

# 删除键值对
del ds['gender']
print(ds)

# 遍历字典
for key in ds:
    print(key, ds[key])

# 成绩字典
scores = {'张三': 90, '李四': 85, '王五': 88}

# 添加
scores['赵六'] = 95
print(scores)

# 删除
pop = scores.pop('李四')
print(pop)
print(scores)

# 获取key
keys = scores.keys()
print(keys)

# 获取value
values = scores.values()
print(values)

# 获取key和value
items = scores.items()
print(items)

# 统计数量
l = len(scores)
print(l)
