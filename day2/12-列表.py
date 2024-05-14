# 列表
nameList = ['张三', '李四', '王五']

for name in nameList:
    print(name)

kklist = list()
kklist.append('a')
kklist.append('b')
kklist.append('c')

print(kklist)
kklist.remove('b')
print(kklist)

# 下标
print(nameList[0])

# 切片
print(nameList[1:3])  # 索引1到2

# 修改
nameList[1] = '李四2'
print(nameList)
print("--------------------------------------------")
kkk = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
for i in range(0, len(kkk)):
    print(i, kkk[i])
